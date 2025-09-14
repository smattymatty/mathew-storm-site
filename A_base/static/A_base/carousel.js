/*!
 * Professional Carousel - Simple Fade Version
 * Clean, professional, no sliding - just fade transitions
 */

(function(d) {
  'use strict';

  class Carousel {
    constructor(element) {
      this.carousel = element;
      this.slides = element.querySelectorAll('.carousel__slide');
      this.totalSlides = this.slides.length;
      this.currentSlide = 0;
      this.moving = false;

      if (this.totalSlides > 1) {
        this.init();
      }
    }

    init() {
      // Set initial state
      this.setInitialState();

      // Add event listeners
      this.setEventListeners();

      // Add touch support
      this.addTouchSupport();

      // Add keyboard support
      this.addKeyboardSupport();
    }

    setInitialState() {
      // Hide all slides except the first one
      this.slides.forEach((slide, index) => {
        slide.classList.remove('initial', 'active');
        if (index === 0) {
          slide.classList.add('active');
        }
      });
    }

    setEventListeners() {
      const prevBtn = this.carousel.querySelector('.carousel__button--prev');
      const nextBtn = this.carousel.querySelector('.carousel__button--next');
      const wrapper = this.carousel.parentElement;
      const dots = wrapper.querySelectorAll('.carousel__dot');

      if (prevBtn) {
        prevBtn.addEventListener('click', () => this.movePrev());
      }

      if (nextBtn) {
        nextBtn.addEventListener('click', () => this.moveNext());
      }

      dots.forEach((dot, index) => {
        dot.addEventListener('click', () => this.moveToSlide(index));
      });
    }

    moveNext() {
      if (!this.moving && this.totalSlides > 1) {
        const nextIndex = (this.currentSlide + 1) % this.totalSlides;
        this.fadeToSlide(nextIndex);
      }
    }

    movePrev() {
      if (!this.moving && this.totalSlides > 1) {
        const prevIndex = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
        this.fadeToSlide(prevIndex);
      }
    }

    moveToSlide(index) {
      if (!this.moving && index !== this.currentSlide && this.totalSlides > 1) {
        this.fadeToSlide(index);
      }
    }

    fadeToSlide(newIndex) {
      if (this.moving) return;

      this.moving = true;

      const currentSlideEl = this.slides[this.currentSlide];
      const newSlideEl = this.slides[newIndex];

      // Fade out current slide
      currentSlideEl.classList.remove('active');

      // Fade in new slide
      newSlideEl.classList.add('active');

      // Update dots
      this.updateDots(newIndex);

      // Update current slide index
      this.currentSlide = newIndex;

      // Re-enable interaction after transition
      setTimeout(() => {
        this.moving = false;
      }, 500); // Match CSS transition duration
    }

    updateDots(activeIndex) {
      const wrapper = this.carousel.parentElement;
      const dots = wrapper.querySelectorAll('.carousel__dot');
      dots.forEach((dot, index) => {
        if (index === activeIndex) {
          dot.classList.add('active');
        } else {
          dot.classList.remove('active');
        }
      });
    }

    addTouchSupport() {
      let touchStartX = 0;
      let touchEndX = 0;

      this.carousel.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      this.carousel.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        this.handleSwipe(touchStartX, touchEndX);
      }, { passive: true });
    }

    handleSwipe(startX, endX) {
      const threshold = 50;
      const diff = startX - endX;

      if (Math.abs(diff) > threshold) {
        if (diff > 0) {
          this.moveNext();
        } else {
          this.movePrev();
        }
      }
    }

    addKeyboardSupport() {
      this.carousel.setAttribute('tabindex', '0');

      this.carousel.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
          e.preventDefault();
          this.movePrev();
        } else if (e.key === 'ArrowRight') {
          e.preventDefault();
          this.moveNext();
        }
      });
    }
  }

  // Initialize all carousels on page load
  function initCarousels() {
    const carousels = d.querySelectorAll('.carousel');
    carousels.forEach(carousel => {
      new Carousel(carousel);
    });
  }

  // Wait for DOM content to load
  if (d.readyState === 'loading') {
    d.addEventListener('DOMContentLoaded', initCarousels);
  } else {
    initCarousels();
  }

  // Reinitialize carousels after HTMX loads
  if (typeof htmx !== 'undefined') {
    d.body.addEventListener('htmx:afterSwap', initCarousels);
  }

}(document));