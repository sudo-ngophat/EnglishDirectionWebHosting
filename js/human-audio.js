(() => {
  const manifestUrl = window.HUMAN_AUDIO_MANIFEST_URL || 'audio/human/manifest.json';
  const vocabManifestUrl = window.VOCAB_AUDIO_MANIFEST_URL || 'audio/vocab/manifest.json';
  const nativeSynth = window.__nativeSpeechSynthesis || window.speechSynthesis;
  const NativeUtterance = window.__NativeSpeechSynthesisUtterance || window.SpeechSynthesisUtterance;
  let manifestPromise = null;
  let vocabManifestPromise = null;
  let currentAudio = null;

  function toRootRelativeUrl(path) {
    const cleanPath = String(path || '').replace(/^\/+/, '');
    const depth = window.location.pathname.split('/').filter(Boolean).length - 1;
    const prefix = depth > 0 ? '../'.repeat(depth) : '';
    return `${prefix}${cleanPath}`;
  }

  async function loadManifest() {
    if (!manifestPromise) {
      manifestPromise = fetch(toRootRelativeUrl(manifestUrl))
        .then(response => {
          if (!response.ok) return {};
          return response.json();
        })
        .catch(() => ({}));
    }
    return manifestPromise;
  }

  async function loadVocabManifest() {
    if (!vocabManifestPromise) {
      vocabManifestPromise = fetch(toRootRelativeUrl(vocabManifestUrl))
        .then(response => {
          if (!response.ok) return {};
          return response.json();
        })
        .catch(() => ({}));
    }
    return vocabManifestPromise;
  }

  function cancel() {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.src = '';
      currentAudio = null;
    }
  }

  function playHumanAudio(url, { rate = 1, onend, onerror } = {}) {
    cancel();
    const audio = new Audio(toRootRelativeUrl(url));
    currentAudio = audio;
    audio.playbackRate = rate;
    audio.onended = () => {
      if (currentAudio === audio) currentAudio = null;
      if (typeof onend === 'function') onend();
    };
    audio.onerror = () => {
      if (currentAudio === audio) currentAudio = null;
      if (typeof onerror === 'function') onerror();
    };
    return audio.play().catch(error => {
      if (currentAudio === audio) currentAudio = null;
      if (typeof onerror === 'function') onerror(error);
    });
  }

  function vocabWordForKey(key) {
    if (!key) return null;
    // key patterns like "dictation:vocabulary:word" or plain word
    const parts = String(key).split(':');
    if (parts.length === 1) return parts[0];
    if (parts[0] === 'dictation' && parts[1] === 'vocabulary' && parts[2]) return parts[2];
    return null;
  }

  async function play({ lessonId, key, text, rate = 1, voice = null, fallback = null, onend = null } = {}) {
    const manifest = await loadManifest();
    const lessonMap = manifest[lessonId] || {};
    const humanUrl = lessonMap[key];

    const nextFallback = () => playNativeTTS({ text, rate, voice, fallback, onend });

    if (humanUrl) {
      return playHumanAudio(humanUrl, {
        rate,
        onend,
        onerror: async () => {
          const vocabUrl = await lookupVocabUrl(lessonId, key);
          if (vocabUrl) {
            return playHumanAudio(vocabUrl, { rate, onend, onerror: nextFallback });
          }
          return nextFallback();
        },
      });
    }

    const vocabUrl = await lookupVocabUrl(lessonId, key);
    if (vocabUrl) {
      return playHumanAudio(vocabUrl, {
        rate,
        onend,
        onerror: nextFallback,
      });
    }

    return nextFallback();
  }

  async function lookupVocabUrl(lessonId, key) {
    if (!lessonId) return null;
    const word = vocabWordForKey(key);
    if (!word) return null;
    const vocabManifest = await loadVocabManifest();
    const lessonMap = vocabManifest[lessonId];
    return lessonMap ? lessonMap[word] : null;
  }

  function playNativeTTS({ text, rate = 1, voice = null, fallback = null, onend = null } = {}) {
    if (typeof fallback === 'function') {
      return fallback();
    }

    if (!text || !nativeSynth || !NativeUtterance) return undefined;
    nativeSynth.cancel();
    const utterance = new NativeUtterance(text);
    utterance.voice = voice;
    utterance.rate = rate;
    utterance.pitch = 1;
    if (typeof onend === 'function') utterance.onend = onend;
    nativeSynth.speak(utterance);
    return undefined;
  }

  window.HumanAudio = {
    loadManifest,
    play,
    playHumanAudio,
    cancel,
  };
})();
