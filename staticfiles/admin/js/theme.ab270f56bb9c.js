'use strict';
{
    window.addEventListener('load', function(e) {

        /**
         * Applies the specified theme mode to the document and saves the preference.
         *
         * If the provided mode is not "light", "dark", or "auto", defaults to "auto".
         *
         * @param {string} mode - The desired theme mode ("light", "dark", or "auto").
         */
        function setTheme(mode) {
            if (mode !== "light" && mode !== "dark" && mode !== "auto") {
                console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
                mode = "auto";
            }
            document.documentElement.dataset.theme = mode;
            localStorage.setItem("theme", mode);
        }

        /**
         * Cycles the website's theme between "auto", "light", and "dark" modes based on the user's system preference.
         *
         * The cycling order adapts to the system's color scheme: if the system prefers dark mode, the sequence is "auto" → "light" → "dark" → "auto"; if it prefers light mode, the sequence is "auto" → "dark" → "light" → "auto".
         */
        function cycleTheme() {
            const currentTheme = localStorage.getItem("theme") || "auto";
            const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

            if (prefersDark) {
                // Auto (dark) -> Light -> Dark
                if (currentTheme === "auto") {
                    setTheme("light");
                } else if (currentTheme === "light") {
                    setTheme("dark");
                } else {
                    setTheme("auto");
                }
            } else {
                // Auto (light) -> Dark -> Light
                if (currentTheme === "auto") {
                    setTheme("dark");
                } else if (currentTheme === "dark") {
                    setTheme("light");
                } else {
                    setTheme("auto");
                }
            }
        }

        /**
         * Initializes the website theme based on the user's saved preference or defaults to auto mode.
         *
         * Applies the theme stored in localStorage if available; otherwise, sets the theme to "auto".
         */
        function initTheme() {
            // set theme defined in localStorage if there is one, or fallback to auto mode
            const currentTheme = localStorage.getItem("theme");
            currentTheme ? setTheme(currentTheme) : setTheme("auto");
        }

        /**
         * Sets up theme toggling functionality by attaching click event listeners to elements with the "theme-toggle" class and initializes the theme on page load.
         */
        function setupTheme() {
            // Attach event handlers for toggling themes
            const buttons = document.getElementsByClassName("theme-toggle");
            Array.from(buttons).forEach((btn) => {
                btn.addEventListener("click", cycleTheme);
            });
            initTheme();
        }

        setupTheme();
    });
}
