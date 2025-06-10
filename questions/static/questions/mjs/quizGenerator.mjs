/**
 * questions/static/questions/mjs/quizGenerator.mjs
 * Handles generation of quiz URLs with current filter parameters
 */

import { formatFiltersForHTMX } from "./utils.mjs";

/**
 * QuizGenerator handles the "Generate Quiz" functionality
 */
class QuizGenerator {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener("DOMContentLoaded", () => {
            this.setupGenerateQuizButton();
        });
    }

    setupGenerateQuizButton() {
        const generateBtn = document.getElementById("generate-quiz-btn");
        if (!generateBtn) {
            console.warn("Generate Quiz button not found");
            return;
        }

        generateBtn.addEventListener("click", () => {
            this.generateQuizUrl();
        });

        console.log("✅ Quiz Generator initialized");
    }

    generateQuizUrl() {
        // Get current filter selections
        const filters = formatFiltersForHTMX();

        console.log("🎯 Generating quiz with filters:", filters);

        // Build quiz URL with parameters
        const quizUrl = new URL("/questions/quiz/", window.location.origin);

        // Map HTMX filter format to quiz URL parameters
        if (filters["tags"]) {
            quizUrl.searchParams.set("tags", filters["tags"]);
        }
        if (filters["title-id"]) {
            quizUrl.searchParams.set("titles", filters["title-id"]);
        }
        if (filters["difficulty"]) {
            quizUrl.searchParams.set("difficulty", filters["difficulty"]);
        }

        console.log("🚀 Redirecting to quiz:", quizUrl.toString());

        // Redirect to quiz page
        window.location.href = quizUrl.toString();
    }
}

// Initialize the quiz generator
export const quizGenerator = new QuizGenerator();
