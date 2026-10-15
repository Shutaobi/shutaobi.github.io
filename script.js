// The page remains usable without JavaScript; native audio controls are the fallback.
(() => {
  const audio = document.getElementById('winter-audio');
  const controls = document.getElementById('music-controls');
  const toggle = document.getElementById('music-toggle');
  const mute = document.getElementById('music-mute');
  const state = document.getElementById('music-state');
  const progress = document.getElementById('music-progress');
  const volume = document.getElementById('music-volume');
  const elapsed = document.getElementById('music-elapsed');
  const duration = document.getElementById('music-duration');
  if (!audio || !controls) return;

  const formatTime = (seconds) => {
    if (!Number.isFinite(seconds)) return '—:—';
    return `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
  };
  const updateTime = () => {
    elapsed.textContent = formatTime(audio.currentTime);
    duration.textContent = formatTime(audio.duration);
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
      progress.disabled = false;
      progress.max = audio.duration;
      progress.value = audio.currentTime;
      progress.setAttribute('aria-valuetext', `${formatTime(audio.currentTime)} of ${formatTime(audio.duration)}`);
    }
  };
  const updatePlayback = () => {
    const playing = !audio.paused;
    toggle.classList.toggle('is-playing', playing);
    toggle.setAttribute('aria-label', playing ? 'Pause music' : 'Play music');
    state.textContent = playing ? 'Playing' : 'Paused';
  };
  const updateVolume = () => {
    const silent = audio.muted || audio.volume === 0;
    mute.setAttribute('aria-pressed', String(silent));
    mute.setAttribute('aria-label', silent ? 'Unmute music' : 'Mute music');
    mute.classList.toggle('is-muted', silent);
    volume.value = audio.volume;
  };
  const reportError = () => {
    state.textContent = 'Audio unavailable';
    toggle.disabled = true;
  };
  const play = async () => {
    try {
      await audio.play();
    } catch (error) {
      if (error.name === 'NotAllowedError') {
        state.textContent = 'Press play to listen';
      } else if (error.name !== 'AbortError') {
        reportError();
      }
    }
  };

  audio.volume = 0.25;
  audio.controls = false;
  controls.hidden = false;
  toggle.addEventListener('click', () => {
    if (audio.paused) play();
    else audio.pause();
  });
  mute.addEventListener('click', () => {
    const silent = audio.muted || audio.volume === 0;
    if (silent && audio.volume === 0) audio.volume = 0.25;
    audio.muted = !silent;
  });
  volume.addEventListener('input', () => {
    audio.volume = Number(volume.value);
    audio.muted = audio.volume === 0;
  });
  progress.addEventListener('input', () => {
    if (Number.isFinite(audio.duration)) audio.currentTime = Number(progress.value);
    updateTime();
  });
  audio.addEventListener('play', updatePlayback);
  audio.addEventListener('pause', updatePlayback);
  audio.addEventListener('timeupdate', updateTime);
  audio.addEventListener('loadedmetadata', updateTime);
  audio.addEventListener('durationchange', updateTime);
  audio.addEventListener('volumechange', updateVolume);
  audio.addEventListener('error', reportError);
  audio.querySelector('source').addEventListener('error', reportError);
  updateTime();
  updateVolume();
  if (audio.error) reportError();
  else play(); // A blocked autoplay attempt leaves the explicit Play button available.
})();
