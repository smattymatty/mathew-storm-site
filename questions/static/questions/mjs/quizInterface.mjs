/**
 * questions/static/questions/mjs/quizInterface.mjs
 * Handles the interactive quiz interface functionality
 */

class QuizInterface {
  constructor() {
    this.currentQuestionIndex = 0;
    this.score = 0;
    this.totalQuestions = 0;
    this.userAnswers = {};
    this.questionElements = [];
    this.init();
  }

  init() {
    document.addEventListener("DOMContentLoaded", () => {
      this.setupQuizInterface();
    });
  }

  setupQuizInterface() {
    console.log("🎯 Setting up quiz interface...");

    // Get all question elements
    this.questionElements = document.querySelectorAll(".quiz-question-item");
    this.totalQuestions = this.questionElements.length;

    console.log("📊 Found", this.totalQuestions, "questions");

    if (this.totalQuestions === 0) {
      console.log("No questions found for quiz interface");
      return;
    }

    // Setup navigation buttons
    this.setupNavigationButtons();

    // Setup automatic answer checking on radio button selection
    this.setupRadioButtonListeners();

    // Setup quiz controls
    this.setupQuizControls();

    // Initialize display
    this.updateDisplay();

    console.log(
      "✅ Quiz Interface initialized with",
      this.totalQuestions,
      "questions",
    );
  }

  setupNavigationButtons() {
    const prevBtn = document.getElementById("prev-question-btn");
    const skipBtn = document.getElementById("skip-question-btn");

    console.log("🔍 Navigation buttons:", { prevBtn, skipBtn });

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        console.log("⬅️ Previous button clicked");
        this.previousQuestion();
      });
    }

    if (skipBtn) {
      skipBtn.addEventListener("click", () => {
        console.log("⏭️ Skip button clicked");
        this.skipCurrentQuestion();
      });
    }
  }

  setupRadioButtonListeners() {
    this.questionElements.forEach((questionElement, index) => {
      const radioButtons = questionElement.querySelectorAll(
        "input[type='radio']",
      );
      const questionId = questionElement.dataset.questionId;
      const correctAnswer = questionElement.dataset.correctAnswer;

      radioButtons.forEach((radio) => {
        radio.addEventListener("change", () => {
          if (radio.checked) {
            console.log(
              `📝 Answer selected for question ${questionId}:`,
              radio.value,
            );
            this.checkAnswer(
              questionId,
              correctAnswer,
              radio.value,
              questionElement,
            );
          }
        });
      });
    });
  }

  setupQuizControls() {
    const restartBtn = document.getElementById("restart-quiz-btn");
    const finishBtn = document.getElementById("finish-quiz-btn");
    const restartModalBtn = document.getElementById("restart-quiz-modal-btn");

    console.log("🔍 Control buttons:", {
      restartBtn,
      finishBtn,
      restartModalBtn,
    });

    if (restartBtn) {
      restartBtn.addEventListener("click", () => {
        console.log("🔄 Restart button clicked");
        this.restartQuiz();
      });
    }

    if (finishBtn) {
      finishBtn.addEventListener("click", () => {
        console.log("🏁 Finish button clicked");
        this.finishQuiz();
      });
    }

    if (restartModalBtn) {
      restartModalBtn.addEventListener("click", () => {
        console.log("🔄 Restart modal button clicked");
        this.restartQuiz();
      });
    }
  }

  checkAnswer(questionId, correctAnswer, userAnswer, questionElement) {
    console.log(
      "🧐 Checking answer for question:",
      questionId,
      "correct:",
      correctAnswer,
      "user:",
      userAnswer,
    );

    const isCorrect = userAnswer === correctAnswer;

    console.log("📝 Answer check result:", {
      userAnswer,
      correctAnswer,
      isCorrect,
    });

    // Store the answer
    this.userAnswers[questionId] = {
      selected: userAnswer,
      correct: correctAnswer,
      isCorrect: isCorrect,
    };

    // Update score
    if (isCorrect) {
      this.score++;
      console.log("🎉 Correct! Score now:", this.score);
    } else {
      console.log("❌ Incorrect. Score remains:", this.score);
    }

    // Show feedback
    this.showAnswerFeedback(
      questionElement,
      isCorrect,
      userAnswer,
      correctAnswer,
    );

    // Disable answer options for this question
    this.disableQuestionAnswers(questionElement);

    // Update display
    this.updateDisplay();

    // Check if quiz is complete
    if (Object.keys(this.userAnswers).length === this.totalQuestions) {
      console.log("🏁 All questions answered! Showing finish button");
      this.showFinishButton();
    }
  }

  showAnswerFeedback(questionElement, isCorrect, userAnswer, correctAnswer) {
    const feedbackDiv = questionElement.querySelector(".answer-feedback");

    const feedbackClass = isCorrect ? "correct" : "incorrect";
    const feedbackIcon = isCorrect ? "✅" : "❌";
    const feedbackText = isCorrect
      ? "Correct!"
      : `Incorrect. The correct answer is ${correctAnswer.toUpperCase()}.`;

    // Check if this is the last question
    const isLastQuestion =
      this.currentQuestionIndex === this.totalQuestions - 1;
    const nextButtonHtml = isLastQuestion
      ? ""
      : `<button class="feedback-next-btn sb-btn sb-btn-primary sb-btn-sm"
                 onclick="quizInterface.nextQuestion()">
           Next Question →
         </button>`;

    feedbackDiv.innerHTML = `
            <div class="feedback-message sb-p-3 sb-rounded-md sb-border feedback-${feedbackClass}">
                <div class="sb-flex sb-items-center sb-justify-between">
                    <div class="sb-flex sb-items-center sb-gap-2">
                        <span class="sb-text-xl">${feedbackIcon}</span>
                        <span class="sb-font-semibold">${feedbackText}</span>
                    </div>
                    <div class="feedback-actions">
                        ${nextButtonHtml}
                    </div>
                </div>
            </div>
        `;

    feedbackDiv.style.display = "block";

    // Highlight correct/incorrect answers
    this.highlightAnswers(questionElement, userAnswer, correctAnswer);
  }

  highlightAnswers(questionElement, userAnswer, correctAnswer) {
    // Use the existing question-block-options class structure
    const answerOptions = questionElement.querySelectorAll(
      ".question-block-options label",
    );

    answerOptions.forEach((option) => {
      const input = option.querySelector("input");
      const value = input.value;

      if (value === correctAnswer) {
        option.classList.add("answer-correct");
      } else if (value === userAnswer && userAnswer !== correctAnswer) {
        option.classList.add("answer-incorrect");
      }
    });
  }

  skipCurrentQuestion() {
    console.log("⏭️ Skipping question", this.currentQuestionIndex + 1);

    const currentQuestion = this.questionElements[this.currentQuestionIndex];
    const questionId = currentQuestion.dataset.questionId;

    // Use HTMX to call your existing skip endpoint
    htmx
      .ajax("POST", `/questions/htmx/skip-question/${questionId}/`, {
        target: "#skip-feedback",
        swap: "innerHTML",
      })
      .then(() => {
        // After successful skip, show the feedback and disable the question
        this.handleSkipResponse(currentQuestion);
      })
      .catch((error) => {
        console.error("Skip request failed:", error);
        // Show fallback feedback
        this.showSkipFallback(currentQuestion);
      });
  }

  handleSkipResponse(questionElement) {
    // The HTMX response will populate #skip-feedback
    // We need to move that content to the question's feedback area
    const skipFeedback = document.getElementById("skip-feedback");
    const questionFeedback = questionElement.querySelector(".answer-feedback");

    if (skipFeedback.innerHTML.trim()) {
      questionFeedback.innerHTML = skipFeedback.innerHTML;
      questionFeedback.style.display = "block";
      skipFeedback.innerHTML = ""; // Clear the temp feedback area
    } else {
      // Fallback if no response
      this.showSkipFallback(questionElement);
    }

    // Disable the question
    this.disableQuestionAnswers(questionElement);

    // Update navigation buttons
    this.updateDisplay();
  }

  showSkipFallback(questionElement) {
    const feedbackDiv = questionElement.querySelector(".answer-feedback");
    feedbackDiv.innerHTML = `
        <div class="feedback-message sb-p-3 sb-rounded-md sb-border sb-bg-gray-100 sb-border-secondary-50">
            <div class="sb-flex sb-items-center sb-justify-between">
                <div class="sb-flex sb-items-center sb-gap-2">
                    <span class="sb-text-xl">⏭️</span>
                    <span class="sb-font-semibold sb-text-gray-700">Question skipped</span>
                </div>
                <div class="feedback-actions">
                    ${
                      this.currentQuestionIndex < this.totalQuestions - 1
                        ? `<button class="feedback-next-btn sb-btn sb-btn-primary sb-btn-sm"
                               onclick="quizInterface.nextQuestion()">
                         Next Question →
                       </button>`
                        : ""
                    }
                </div>
            </div>
        </div>
    `;
    feedbackDiv.style.display = "block";
  }

  disableQuestionAnswers(questionElement) {
    const inputs = questionElement.querySelectorAll("input[type='radio']");

    inputs.forEach((input) => {
      input.disabled = true;
    });
  }

  scrollToCurrentQuestion() {
    if (this.questionElements[this.currentQuestionIndex]) {
      const currentQuestion = this.questionElements[this.currentQuestionIndex];

      // Scroll to the top of the current question with smooth behavior
      currentQuestion.scrollIntoView({
        behavior: "smooth",
        block: "start",
        inline: "nearest",
      });

      // Alternative: scroll to a bit above the question for better visibility
      setTimeout(() => {
        const rect = currentQuestion.getBoundingClientRect();
        const offset = 20; // 20px above the question
        window.scrollBy({
          top: rect.top - offset,
          behavior: "smooth",
        });
      }, 100);
    }
  }

  previousQuestion() {
    if (this.currentQuestionIndex > 0) {
      this.currentQuestionIndex--;
      console.log("⬅️ Moving to question", this.currentQuestionIndex + 1);
      this.showCurrentQuestion();
      this.updateDisplay();
      this.scrollToCurrentQuestion();
    }
  }

  nextQuestion() {
    if (this.currentQuestionIndex < this.totalQuestions - 1) {
      this.currentQuestionIndex++;
      console.log("➡️ Moving to question", this.currentQuestionIndex + 1);
      this.showCurrentQuestion();
      this.updateDisplay();
      this.scrollToCurrentQuestion();
    }
  }

  showCurrentQuestion() {
    this.questionElements.forEach((element, index) => {
      element.style.display =
        index === this.currentQuestionIndex ? "block" : "none";
    });
  }

  updateDisplay() {
    // Update current question number
    const currentQuestionNum = document.getElementById("current-question-num");
    if (currentQuestionNum) {
      currentQuestionNum.textContent = this.currentQuestionIndex + 1;
    }

    // Update score
    const scoreDisplay = document.getElementById("score-display");
    if (scoreDisplay) {
      scoreDisplay.textContent = `${this.score}/${Object.keys(this.userAnswers).length}`;
    }

    // Update progress bar
    const progressBar = document.getElementById("progress-bar");
    if (progressBar) {
      const answeredQuestions = Object.keys(this.userAnswers).length;
      const progressPercentage =
        (answeredQuestions / this.totalQuestions) * 100;
      progressBar.style.width = `${progressPercentage}%`;
    }

    // Update navigation buttons
    this.updateNavigationButtons();
  }

  updateNavigationButtons() {
    const prevBtn = document.getElementById("prev-question-btn");
    const skipBtn = document.getElementById("skip-question-btn");

    if (prevBtn) {
      prevBtn.disabled = this.currentQuestionIndex === 0;
    }

    if (skipBtn) {
      // Disable skip button if question is already answered or skipped
      const currentQuestion = this.questionElements[this.currentQuestionIndex];
      const questionId = currentQuestion.dataset.questionId;
      const isAnswered = this.userAnswers.hasOwnProperty(questionId);
      const feedbackVisible =
        currentQuestion.querySelector(".answer-feedback").style.display !==
        "none";

      skipBtn.disabled = isAnswered || feedbackVisible;
    }
  }

  showFinishButton() {
    const finishBtn = document.getElementById("finish-quiz-btn");
    if (finishBtn) {
      finishBtn.style.display = "inline-block";
    }
  }

  finishQuiz() {
    // Calculate final results
    const totalAnswered = Object.keys(this.userAnswers).length;
    const percentage = Math.round((this.score / totalAnswered) * 100);

    // Update modal content
    const finalScoreElement = document.getElementById("final-score");
    const scorePercentageElement = document.getElementById("score-percentage");

    if (finalScoreElement) {
      finalScoreElement.textContent = `${this.score}/${totalAnswered}`;
    }

    if (scorePercentageElement) {
      scorePercentageElement.textContent = `${percentage}%`;
    }

    // Show completion modal
    const modal = document.getElementById("quiz-completion-modal");
    if (modal) {
      modal.style.display = "block";
    }

    console.log("🎉 Quiz completed!", {
      score: this.score,
      total: totalAnswered,
      percentage,
    });
  }

  restartQuiz() {
    // Reset all state
    this.currentQuestionIndex = 0;
    this.score = 0;
    this.userAnswers = {};

    // Hide completion modal
    const modal = document.getElementById("quiz-completion-modal");
    if (modal) {
      modal.style.display = "none";
    }

    // Hide finish button
    const finishBtn = document.getElementById("finish-quiz-btn");
    if (finishBtn) {
      finishBtn.style.display = "none";
    }

    // Reset all question states
    this.questionElements.forEach((questionElement) => {
      // Re-enable all inputs
      const inputs = questionElement.querySelectorAll("input[type='radio']");
      inputs.forEach((input) => {
        input.disabled = false;
        input.checked = false;
      });

      // Hide feedback
      const feedbackDiv = questionElement.querySelector(".answer-feedback");
      if (feedbackDiv) {
        feedbackDiv.style.display = "none";
        feedbackDiv.innerHTML = "";
      }

      // Remove answer highlighting - use proper class selector
      const answerOptions = questionElement.querySelectorAll(
        ".question-block-options label",
      );
      answerOptions.forEach((option) => {
        option.classList.remove("answer-correct", "answer-incorrect");
      });
    });

    // Show first question
    this.showCurrentQuestion();

    // Update display
    this.updateDisplay();

    // Scroll to first question
    this.scrollToCurrentQuestion();

    console.log("🔄 Quiz restarted");
  }
}

// Initialize the quiz interface
//export const quizInterface = new QuizInterface();

// Initialize the quiz interface and make it globally accessible
const quizInterface = new QuizInterface();

// Make it available globally for button onclick handlers
window.quizInterface = quizInterface;

export { quizInterface };
