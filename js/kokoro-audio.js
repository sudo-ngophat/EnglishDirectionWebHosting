(() => {
  const apiUrl = window.KOKORO_TTS_URL || 'http://127.0.0.1:8000/api/v1/tts/render';
  const mode = window.KOKORO_TTS_MODE || 'lesson';
  const nativeSpeechSynthesis = window.speechSynthesis;
  const NativeSpeechSynthesisUtterance = window.SpeechSynthesisUtterance;

  if (nativeSpeechSynthesis && !window.__nativeSpeechSynthesis) {
    Object.defineProperty(window, '__nativeSpeechSynthesis', {
      configurable: true,
      value: nativeSpeechSynthesis,
    });
  }

  if (NativeSpeechSynthesisUtterance && !window.__NativeSpeechSynthesisUtterance) {
    Object.defineProperty(window, '__NativeSpeechSynthesisUtterance', {
      configurable: true,
      value: NativeSpeechSynthesisUtterance,
    });
  }
  const voices = Object.freeze([
    {
      name: 'Kokoro Teacher',
      lang: 'en-US',
      voiceURI: 'kokoro-teacher',
      default: true,
      localService: false,
    },
  ]);

  class KokoroUtterance {
    constructor(text = '') {
      this.text = String(text);
      this.voice = null;
      this.rate = 1;
      this.pitch = 1;
      this.volume = 1;
      this.lang = 'en-US';
      this.onend = null;
      this.onerror = null;
    }
  }

  class KokoroSpeechSynthesis {
    constructor() {
      this._audio = null;
      this._url = null;
      this._abortController = null;
      this._onvoiceschanged = null;
      this._speaking = false;
      this._paused = false;
      this._token = 0;
      setTimeout(() => this._emitVoicesChanged(), 0);
    }

    get speaking() {
      return this._speaking;
    }

    get pending() {
      return false;
    }

    get paused() {
      return this._paused;
    }

    get onvoiceschanged() {
      return this._onvoiceschanged;
    }

    set onvoiceschanged(handler) {
      this._onvoiceschanged = typeof handler === 'function' ? handler : null;
      if (this._onvoiceschanged) {
        setTimeout(() => this._emitVoicesChanged(), 0);
      }
    }

    getVoices() {
      return [...voices];
    }

    cancel() {
      this._token += 1;
      this._stopPlayback();
      this._speaking = false;
      this._paused = false;
    }

    pause() {
      if (!this._audio || this._audio.paused) {
        return;
      }
      this._audio.pause();
      this._paused = true;
    }

    resume() {
      if (!this._audio || !this._paused) {
        return;
      }
      this._audio.play().catch(() => {});
      this._paused = false;
    }

    async speak(utterance) {
      if (!utterance) {
        return;
      }

      const text = String(utterance.text || '').trim();
      if (!text) {
        return;
      }

      const token = this._token + 1;
      this._token = token;
      this._stopPlayback();
      this._speaking = true;
      this._paused = false;

      const abortController = new AbortController();
      this._abortController = abortController;

      try {
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text, mode }),
          signal: abortController.signal,
        });

        if (!response.ok) {
          throw new Error(`TTS request failed with ${response.status}`);
        }

        const blob = await response.blob();
        if (token !== this._token) {
          return;
        }

        const audio = new Audio();
        const url = URL.createObjectURL(blob);
        audio.src = url;
        audio.preload = 'auto';
        audio.playbackRate = this._normalizeRate(utterance.rate);
        audio.volume = this._normalizeVolume(utterance.volume);

        this._audio = audio;
        this._url = url;

        audio.onended = () => {
          if (token !== this._token) {
            return;
          }
          this._speaking = false;
          this._paused = false;
          this._cleanupUrl();
          this._audio = null;
          if (typeof utterance.onend === 'function') {
            utterance.onend();
          }
        };

        audio.onerror = () => {
          if (token !== this._token) {
            return;
          }
          this._speaking = false;
          this._paused = false;
          this._cleanupUrl();
          this._audio = null;
          if (typeof utterance.onerror === 'function') {
            utterance.onerror(new Error('Audio playback failed'));
          }
        };

        await audio.play();
      } catch (error) {
        if (abortController.signal.aborted || token !== this._token) {
          return;
        }
        this._speaking = false;
        this._paused = false;
        this._stopPlayback();
        if (typeof utterance.onerror === 'function') {
          utterance.onerror(error);
        }
      }
    }

    _emitVoicesChanged() {
      if (typeof this._onvoiceschanged === 'function') {
        this._onvoiceschanged();
      }
    }

    _normalizeRate(rate) {
      const value = Number(rate);
      if (!Number.isFinite(value)) {
        return 1;
      }
      return Math.min(2, Math.max(0.5, value));
    }

    _normalizeVolume(volume) {
      const value = Number(volume);
      if (!Number.isFinite(value)) {
        return 1;
      }
      return Math.min(1, Math.max(0, value));
    }

    _cleanupUrl() {
      if (!this._url) {
        return;
      }
      URL.revokeObjectURL(this._url);
      this._url = null;
    }

    _stopPlayback() {
      if (this._abortController) {
        this._abortController.abort();
        this._abortController = null;
      }
      if (this._audio) {
        this._audio.pause();
        this._audio.src = '';
        this._audio = null;
      }
      this._cleanupUrl();
    }
  }

  Object.defineProperty(window, 'SpeechSynthesisUtterance', {
    configurable: true,
    writable: true,
    value: KokoroUtterance,
  });

  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: new KokoroSpeechSynthesis(),
  });
})();
