class Slider {
  constructor(config) {
    this.slides = Array.from(document.querySelectorAll('.slide'));
    this.wrapper = document.getElementById('sliderWrapper');
    this.counter = document.getElementById('counter');
    this.pagination = document.getElementById('pagination');
    this.index = 0;
    this.timer = null;

    this.settings = {
      loop: config.loop,
      navs: config.navs,
      pags: config.pags,
      auto: config.auto,
      stopMouseHover: config.stopMouseHover,
      delay: config.delay * 1000
    };

    this.init();
  }

  init() {
    this.update();
    this.applyNavs();
    this.applyPags();
    if (this.settings.auto) this.startAuto();
    if (this.settings.stopMouseHover) this.addHoverListeners();
  }

  applyNavs() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    if (!prevBtn || !nextBtn) return;

    if (this.settings.navs) {
      prevBtn.style.display = 'inline-block';
      nextBtn.style.display = 'inline-block';
      prevBtn.onclick = () => this.prev();
      nextBtn.onclick = () => this.next();
    } else {
      prevBtn.style.display = 'none';
      nextBtn.style.display = 'none';
      prevBtn.onclick = null;
      nextBtn.onclick = null;
    }
  }

  applyPags() {
    if (this.settings.pags) {
      this.renderPagination();
    } else {
      this.pagination.innerHTML = '';
    }
  }

  renderPagination() {
    this.pagination.innerHTML = '';
    this.slides.forEach((_, i) => {
      const btn = document.createElement('button');
      btn.addEventListener('click', () => this.goTo(i));
      this.pagination.appendChild(btn);
    });
    this.updatePagination();
  }

  updatePagination() {
    [...this.pagination.children].forEach((btn, i) => {
      btn.classList.toggle('active', i === this.index);
    });
  }

  updateCounter() {
    this.counter.textContent = `${this.index + 1}/${this.slides.length}`;
  }

  goTo(i) {
    this.index = i;
    this.update();
  }

  next() {
    if (this.index < this.slides.length - 1) {
      this.index++;
    } else if (this.settings.loop) {
      this.index = 0;
    }
    this.update();
  }

  prev() {
    if (this.index > 0) {
      this.index--;
    } else if (this.settings.loop) {
      this.index = this.slides.length - 1;
    }
    this.update();
  }

  update() {
    this.wrapper.style.transform = `translateX(-${this.index * 100}%)`;
    this.updateCounter();
    this.updatePagination();
  }

  startAuto() {
    this.stopAuto();
    if (this.settings.delay >= 1000) {
      this.timer = setInterval(() => this.next(), this.settings.delay);
    }
  }

  stopAuto() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  addHoverListeners() {
    this._hoverIn = () => this.stopAuto();
    this._hoverOut = () => this.startAuto();
    this.wrapper.addEventListener('mouseenter', this._hoverIn);
    this.wrapper.addEventListener('mouseleave', this._hoverOut);
  }

  removeHoverListeners() {
    if (this._hoverIn && this._hoverOut) {
      this.wrapper.removeEventListener('mouseenter', this._hoverIn);
      this.wrapper.removeEventListener('mouseleave', this._hoverOut);
      this._hoverIn = null;
      this._hoverOut = null;
    }
  }

  updateSettings(newSettings) {
    if (!newSettings.delay || newSettings.delay < 1) {
      newSettings.delay = 5;
    }
    newSettings.delay = newSettings.delay * 1000;
    Object.assign(this.settings, newSettings);

    this.stopAuto();
    if (this.settings.auto) this.startAuto();

    this.applyNavs();
    this.applyPags();

    this.removeHoverListeners();
    if (this.settings.stopMouseHover) this.addHoverListeners();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const slider = new Slider({
    loop: true,
    navs: true,
    pags: true,
    auto: true,
    stopMouseHover: true,
    delay: 5
  });

  const applyBtn = document.getElementById('applySettings');
  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      slider.updateSettings({
        loop: document.getElementById('loopInput').checked,
        navs: document.getElementById('navsInput').checked,
        pags: document.getElementById('pagsInput').checked,
        auto: document.getElementById('autoInput').checked,
        stopMouseHover: document.getElementById('hoverStopInput').checked,
        delay: +document.getElementById('delayInput').value || 5
      });
    });
  }
});
