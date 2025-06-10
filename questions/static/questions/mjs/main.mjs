/**
 * questions/static/questions/mjs/main.mjs
 * Main entry point for quiz functionality
 */

import { quizHTMXHandler } from "./htmxHandler.mjs";
import { debugFilters } from "./utils.mjs";

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  console.log("🎯 Quiz MJS modules loaded");

  // Add debug function to window for console access
  window.debugQuizFilters = debugFilters;
});
