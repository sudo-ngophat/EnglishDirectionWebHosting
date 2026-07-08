(() => {
  const STORAGE_KEY = 'audio_engine';
  const DEFAULT_MODE = 'wav';
  const KOKORO_PORT = window.KOKORO_TTS_PORT || 8000;
  const isLocalHost = /^(localhost|127\.0\.0\.1|10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)/.test(window.location.hostname);
  const kokoroHost = window.location.hostname && isLocalHost ? window.location.hostname : '127.0.0.1';
  const kokoroBase = `http://${kokoroHost}:${KOKORO_PORT}`;
  const KOKORO_URL = window.KOKORO_TTS_URL || `${kokoroBase}/api/v1/tts/render`;
  const KOKORO_MODE = window.KOKORO_TTS_MODE || 'lesson';
  const KOKORO_HEALTH_URL = window.KOKORO_HEALTH_URL || `${kokoroBase}/api/v1/health`;
  const nativeSynth = window.__nativeSpeechSynthesis || window.speechSynthesis;
  const NativeUtterance = window.__NativeSpeechSynthesisUtterance || window.SpeechSynthesisUtterance;

  const listeners = new Set();
  let currentAudio = null;
  let currentUrl = null;
  let currentAbort = null;
  let token = 0;

  function getMode() {
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      return value === 'kokoro' ? 'kokoro' : DEFAULT_MODE;
    } catch {
      return DEFAULT_MODE;
    }
  }

  function setMode(mode) {
    const normalized = mode === 'kokoro' ? 'kokoro' : 'wav';
    try {
      localStorage.setItem(STORAGE_KEY, normalized);
    } catch {}
    listeners.forEach((fn) => {
      try { fn(normalized); } catch {}
    });
    return normalized;
  }

  function onChange(fn) {
    if (typeof fn === 'function') listeners.add(fn);
    return () => listeners.delete(fn);
  }

  function stopCurrent() {
    token += 1;
    if (currentAbort) {
      try { currentAbort.abort(); } catch {}
      currentAbort = null;
    }
    if (currentAudio) {
      try { currentAudio.pause(); } catch {}
      currentAudio.src = '';
      currentAudio = null;
    }
    if (currentUrl) {
      try { URL.revokeObjectURL(currentUrl); } catch {}
      currentUrl = null;
    }
    if (window.HumanAudio && typeof window.HumanAudio.cancel === 'function') {
      window.HumanAudio.cancel();
    }
  }

  async function healthCheck() {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 1500);
      const response = await fetch(KOKORO_HEALTH_URL, { signal: controller.signal });
      clearTimeout(timer);
      return response.ok;
    } catch {
      return false;
    }
  }

  function playNative(options) {
    const opts = options || {};
    const text = String(opts.text || '').trim();
    if (!text || !nativeSynth || !NativeUtterance) return null;
    nativeSynth.cancel();
    const utterance = new NativeUtterance(text);
    utterance.voice = opts.voice || null;
    utterance.rate = opts.rate || 1;
    if (typeof opts.onend === 'function') utterance.onend = opts.onend;
    nativeSynth.speak(utterance);
    return utterance;
  }

  function playWav(options) {
    if (window.HumanAudio && typeof window.HumanAudio.play === 'function') {
      return window.HumanAudio.play(options || {});
    }
    return playNative(options);
  }

  async function playKokoro(options) {
    const text = String(options && options.text || '').trim();
    if (!text) return playWav(options);

    stopCurrent();
    const myToken = ++token;
    const abort = new AbortController();
    currentAbort = abort;

    try {
      const response = await fetch(KOKORO_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, mode: KOKORO_MODE }),
        signal: abort.signal,
      });
      if (!response.ok) throw new Error('kokoro http ' + response.status);

      const blob = await response.blob();
      if (myToken !== token) return null;

      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.playbackRate = options && options.rate ? Number(options.rate) || 1 : 1;

      currentAudio = audio;
      currentUrl = url;

      const finish = () => {
        if (myToken !== token) return;
        stopCurrent();
        if (options && typeof options.onend === 'function') options.onend();
      };
      const fail = () => {
        if (myToken !== token) return;
        stopCurrent();
        playWav(options);
      };

      audio.onended = finish;
      audio.onerror = fail;

      await audio.play();
      return audio;
    } catch (error) {
      if (myToken !== token) return null;
      stopCurrent();
      return playWav(options);
    }
  }

  function play(options) {
    const opts = options || {};
    if (getMode() === 'kokoro') {
      return playKokoro(opts);
    }
    stopCurrent();
    return playWav(opts);
  }

  function cancel() {
    stopCurrent();
  }

  window.AudioEngine = {
    getMode,
    setMode,
    onChange,
    play,
    cancel,
    healthCheck,
  };
})();
