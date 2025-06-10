/**
 * questions/static/questions/mjs/mystery.mjs
 * Handles the mystery of making HTMX work with selected pills
 */

import {
  formatFiltersForHTMX,
  debugFilters,
  hasSelectedFilters,
} from "./utils.mjs";

/**
 * QuizHTMXHandler manages the HTMX integration for question loading
 */
class QuizHTMXHandler {
  constructor() {
    this.loadButton = null;
    this.init();
  }

  init() {
    // Wait for DOM to be ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => this.setup());
    } else {
      this.setup();
    }
  }

  setup() {
    this.loadButton = document.querySelector(".sb-btn-white[hx-get]");
    if (!this.loadButton) {
      console.error("Load Questions button not found");
      return;
    }

    // Remove the original click handler and add our custom one
    this.setupCustomClickHandler();

    console.log("✅ QuizHTMXHandler initialized");
  }

  setupCustomClickHandler() {
    // Remove HTMX attributes to prevent default behavior
    const htmxUrl = this.loadButton.getAttribute("hx-get");
    const htmxTarget = this.loadButton.getAttribute("hx-target");
    const htmxSwap = this.loadButton.getAttribute("hx-swap");
    const htmxIndicator = this.loadButton.getAttribute("hx-indicator");

    // Store these for our custom request
    this.htmxConfig = {
      url: htmxUrl,
      target: htmxTarget,
      swap: htmxSwap,
      indicator: htmxIndicator,
    };

    // Remove HTMX attributes
    this.loadButton.removeAttribute("hx-get");
    this.loadButton.removeAttribute("hx-vals");

    // Add our custom click handler
    this.loadButton.addEventListener("click", (e) => {
      e.preventDefault();
      this.handleLoadQuestions();
    });
  }

  handleLoadQuestions() {
    const filters = formatFiltersForHTMX();

    // Debug output
    debugFilters();

    // Show loading indicator
    const indicator = document.querySelector(this.htmxConfig.indicator);
    if (indicator) {
      indicator.style.display = "block";
    }

    // Create HTMX request with collected filters
    this.makeHTMXRequest(filters);
  }

  makeHTMXRequest(filters) {
    const target = document.querySelector(this.htmxConfig.target);
    if (!target) {
      console.error("HTMX target not found:", this.htmxConfig.target);
      return;
    }

    // Build query string
    const params = new URLSearchParams(filters);
    const url = `${this.htmxConfig.url}?${params.toString()}`;

    console.log("🚀 Making HTMX request:", url);

    // Make the request using HTMX
    htmx
      .ajax("GET", url, {
        target: this.htmxConfig.target,
        swap: this.htmxConfig.swap,
      })
      .then(() => {
        console.log("✅ HTMX request completed");
        this.hideLoadingIndicator();
      })
      .catch((error) => {
        console.error("❌ HTMX request failed:", error);
        this.hideLoadingIndicator();
      });
  }

  hideLoadingIndicator() {
    const indicator = document.querySelector(this.htmxConfig.indicator);
    if (indicator) {
      indicator.style.display = "none";
    }
  }
}

// Initialize the handler
export const quizHTMXHandler = new QuizHTMXHandler();
