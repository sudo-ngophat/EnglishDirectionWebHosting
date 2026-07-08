(() => {
  if (!window.AudioEngine) return;

  const style = document.createElement('style');
  style.textContent = `
    .audio-engine-chip {
      position: fixed;
      top: 12px;
      right: 12px;
      z-index: 9999;
      border: 1px solid rgba(255,255,255,0.25);
      border-radius: 999px;
      padding: 9px 13px;
      background: rgba(15, 23, 42, 0.92);
      color: #fff;
      font: 600 13px/1.2 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      box-shadow: 0 8px 24px rgba(0,0,0,0.22);
      cursor: pointer;
      user-select: none;
    }
    .audio-engine-chip[data-mode="kokoro"] {
      background: rgba(22, 101, 52, 0.94);
    }
    .audio-engine-chip[data-status="error"] {
      background: rgba(185, 28, 28, 0.94);
    }
  `;
  document.head.appendChild(style);

  const chip = document.createElement('button');
  chip.type = 'button';
  chip.className = 'audio-engine-chip';
  document.body.appendChild(chip);

  let busy = false;
  let timer = null;

  function label(text, status) {
    chip.textContent = text;
    chip.dataset.mode = window.AudioEngine.getMode();
    chip.dataset.status = status || 'ok';
  }

  function render() {
    const mode = window.AudioEngine.getMode();
    label(mode === 'kokoro' ? 'Audio: Kokoro' : 'Audio: WAV', 'ok');
  }

  function flash(text, status) {
    clearTimeout(timer);
    label(text, status || 'ok');
    timer = setTimeout(render, 1800);
  }

  chip.addEventListener('click', async () => {
    if (busy) return;
    busy = true;
    const mode = window.AudioEngine.getMode();

    if (mode === 'kokoro') {
      window.AudioEngine.setMode('wav');
      render();
      busy = false;
      return;
    }

    label('Checking Kokoro...', 'ok');
    const ok = await window.AudioEngine.healthCheck();
    if (ok) {
      window.AudioEngine.setMode('kokoro');
      render();
    } else {
      window.AudioEngine.setMode('wav');
      flash('Kokoro chưa bật', 'error');
    }
    busy = false;
  });

  window.AudioEngine.onChange(render);
  render();
})();
