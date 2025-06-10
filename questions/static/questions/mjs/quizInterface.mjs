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

    // Setup answer checking
    this.setupAnswerChecking();

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
    const nextBtn = document.getElementById("next-question-btn");

    console.log("🔍 Navigation buttons:", { prevBtn, nextBtn });

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        console.log("⬅️ Previous button clicked");
        this.previousQuestion();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        console.log("➡️ Next button clicked");
        this.nextQuestion();
      });
    }
  }

  setupAnswerChecking() {
    const checkBtns = document.querySelectorAll(".check-answer-btn");

    console.log("🔍 Found", checkBtns.length, "check answer buttons");

    checkBtns.forEach((btn, index) => {
      console.log(`Setting up check button ${index + 1}:`, btn);
      btn.addEventListener("click", (e) => {
        console.log("✅ Check answer button clicked", e.target);
        const questionId = e.target.dataset.questionId;
        const correctAnswer = e.target.dataset.correctAnswer;
        this.checkAnswer(questionId, correctAnswer, e.target);
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

  checkAnswer(questionId, correctAnswer, buttonElement) {
    console.log(
      "🧐 Checking answer for question:",
      questionId,
      "correct:",
      correctAnswer,
    );

    const questionElement = buttonElement.closest(".quiz-question-item");
    const selectedAnswer = questionElement.querySelector(
      `input[name="answer_for_q${questionId}"]:checked`,
    );

    if (!selectedAnswer) {
      console.warn("❌ No answer selected");
      alert("Please select an answer before checking.");
      return;
    }

    const userAnswer = selectedAnswer.value;
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

    // Disable answer options and check button
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

    feedbackDiv.innerHTML = `
            <div class="feedback-message sb-p-3 sb-rounded-md sb-border feedback-${feedbackClass}">
                <div class="sb-flex sb-items-center sb-mb-2">
                    <span class="sb-text-xl sb-mr-2">${feedbackIcon}</span>
                    <span class="sb-font-semibold">${feedbackText}</span>
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

  disableQuestionAnswers(questionElement) {
    const inputs = questionElement.querySelectorAll("input[type='radio']");
    const checkBtn = questionElement.querySelector(".check-answer-btn");

    inputs.forEach((input) => {
      input.disabled = true;
    });

    if (checkBtn) {
      checkBtn.disabled = true;
      checkBtn.textContent = "Answered";
    }
  }

  previousQuestion() {
    if (this.currentQuestionIndex > 0) {
      this.currentQuestionIndex--;
      console.log("⬅️ Moving to question", this.currentQuestionIndex + 1);
      this.showCurrentQuestion();
      this.updateDisplay();
    }
  }

  nextQuestion() {
    if (this.currentQuestionIndex < this.totalQuestions - 1) {
      this.currentQuestionIndex++;
      console.log("➡️ Moving to question", this.currentQuestionIndex + 1);
      this.showCurrentQuestion();
      this.updateDisplay();
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
    const nextBtn = document.getElementById("next-question-btn");

    if (prevBtn) {
      prevBtn.disabled = this.currentQuestionIndex === 0;
    }

    if (nextBtn) {
      nextBtn.disabled = this.currentQuestionIndex === this.totalQuestions - 1;
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

      // Reset check button
      const checkBtn = questionElement.querySelector(".check-answer-btn");
      if (checkBtn) {
        checkBtn.disabled = false;
        checkBtn.textContent = "Check Answer";
      }

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

    console.log("🔄 Quiz restarted");
  }
}

// Initialize the quiz interface
export const quizInterface = new QuizInterface();
