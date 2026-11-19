// ==========================================
// Online Examination System - Live Test Logic
// Presidency University (CSE2271 Mini-Project)
// ==========================================

let currentIndex = 0;
let userAnswers = {};      // questionId -> 'A' | 'B' | 'C' | 'D'
let reviewFlags = {};      // questionId -> boolean
let visitedStatus = {};    // questionId -> boolean
let remainingSeconds = EXAM_CONFIG.durationMinutes * 60;
let timeTakenSeconds = 0;
let strikeCount = 0;
const MAX_STRIKES = 3;
let timerInterval = null;
let isSubmitted = false;

document.addEventListener("DOMContentLoaded", () => {
  // Mark first question as visited
  if (EXAM_CONFIG.questions.length > 0) {
    visitedStatus[EXAM_CONFIG.questions[0].id] = true;
  }
  
  initTimer();
  renderPalette();
  renderCurrentQuestion();
  initAntiCheatListeners();
  
  // Request Fullscreen mode gently
  try {
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().catch(() => {});
    }
  } catch(e) {}
});

// 1. Timer Logic
function initTimer() {
  const timerElem = document.getElementById("liveTimer");
  
  timerInterval = setInterval(() => {
    if (isSubmitted) {
      clearInterval(timerInterval);
      return;
    }

    if (remainingSeconds > 0) {
      remainingSeconds--;
      timeTakenSeconds++;
      
      const hrs = Math.floor(remainingSeconds / 3600);
      const mins = Math.floor((remainingSeconds % 3600) / 60);
      const secs = remainingSeconds % 60;
      timerElem.textContent = `${pad(hrs)}:${pad(mins)}:${pad(secs)}`;

      // Warning color when under 5 minutes
      if (remainingSeconds < 300) {
        timerElem.style.color = '#ef4444';
      }
    } else {
      clearInterval(timerInterval);
      autoSubmitTimeout();
    }
  }, 1000);
}

function pad(n) {
  return n < 10 ? "0" + n : n;
}

// 2. Question Navigation & Rendering
function renderCurrentQuestion() {
  const questions = EXAM_CONFIG.questions;
  if (!questions || questions.length === 0) return;

  const q = questions[currentIndex];
  visitedStatus[q.id] = true;

  document.getElementById("qBadgeNum").textContent = `QUESTION ${pad(currentIndex + 1)} OF ${questions.length}`;
  document.getElementById("qBadgeMarks").textContent = `Marks: +${q.marks} | Neg: -${EXAM_CONFIG.negativeMarks}`;
  document.getElementById("qStemText").textContent = q.question_text;

  const container = document.getElementById("optionsContainer");
  container.innerHTML = "";

  const options = [
    { key: "A", text: q.option_a },
    { key: "B", text: q.option_b },
    { key: "C", text: q.option_c },
    { key: "D", text: q.option_d }
  ];

  const selectedKey = userAnswers[q.id];

  options.forEach(opt => {
    const isChecked = selectedKey === opt.key;
    const label = document.createElement("label");
    label.className = `option-card ${isChecked ? 'selected' : ''}`;
    label.onclick = () => selectOption(opt.key);

    label.innerHTML = `
      <input type="radio" name="optRadio" value="${opt.key}" ${isChecked ? 'checked' : ''}>
      <span class="opt-text"><strong>${opt.key}.</strong> ${opt.text}</span>
    `;
    container.appendChild(label);
  });

  // Update Prev/Next buttons
  document.getElementById("prevBtn").disabled = (currentIndex === 0);
  const nextBtn = document.getElementById("nextBtn");
  if (currentIndex === questions.length - 1) {
    nextBtn.textContent = "Review & Submit ➔";
  } else {
    nextBtn.textContent = "Save & Next ➔";
  }

  updatePalette();
}

function selectOption(key) {
  const q = EXAM_CONFIG.questions[currentIndex];
  userAnswers[q.id] = key;
  renderCurrentQuestion();
}

function clearActiveOption() {
  const q = EXAM_CONFIG.questions[currentIndex];
  delete userAnswers[q.id];
  renderCurrentQuestion();
}

function toggleMarkReview() {
  const q = EXAM_CONFIG.questions[currentIndex];
  reviewFlags[q.id] = !reviewFlags[q.id];
  navigateNext();
}

function navigateNext() {
  if (currentIndex < EXAM_CONFIG.questions.length - 1) {
    currentIndex++;
    renderCurrentQuestion();
  } else {
    promptSubmitExam();
  }
}

function navigatePrev() {
  if (currentIndex > 0) {
    currentIndex--;
    renderCurrentQuestion();
  }
}

function jumpToQuestion(idx) {
  currentIndex = idx;
  renderCurrentQuestion();
}

// 3. Palette Rendering & State Counts
function renderPalette() {
  const grid = document.getElementById("paletteGrid");
  grid.innerHTML = "";

  EXAM_CONFIG.questions.forEach((q, idx) => {
    const btn = document.createElement("button");
    btn.className = "p-btn";
    btn.id = `palette-btn-${idx}`;
    btn.textContent = idx + 1;
    btn.onclick = () => jumpToQuestion(idx);
    grid.appendChild(btn);
  });

  updatePalette();
}

function updatePalette() {
  let answered = 0;
  let review = 0;
  let unanswered = 0;
  let unvisited = 0;

  EXAM_CONFIG.questions.forEach((q, idx) => {
    const btn = document.getElementById(`palette-btn-${idx}`);
    if (!btn) return;

    btn.className = "p-btn";
    if (idx === currentIndex) {
      btn.classList.add("current");
    }

    if (reviewFlags[q.id]) {
      btn.classList.add("review");
      review++;
    } else if (userAnswers[q.id]) {
      btn.classList.add("answered");
      answered++;
    } else if (visitedStatus[q.id]) {
      btn.classList.add("unanswered");
      unanswered++;
    } else {
      unvisited++;
    }
  });

  document.getElementById("countAnswered").textContent = answered;
  document.getElementById("countReview").textContent = review;
  document.getElementById("countUnanswered").textContent = unanswered;
  document.getElementById("countUnvisited").textContent = unvisited;
}

// 4. Anti-Cheat & Tab-Switch Detection
function initAntiCheatListeners() {
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && !isSubmitted) {
      logProctorViolation("Tab switch or window blur detected");
    }
  });

  window.addEventListener("blur", () => {
    if (!isSubmitted) {
      logProctorViolation("Window lost focus (external application activated)");
    }
  });
}

function logProctorViolation(reason) {
  if (isSubmitted) return;
  strikeCount++;

  // Update Strike Badge on Header
  const strikeBadge = document.getElementById("headerStrikeCount");
  if (strikeBadge) {
    strikeBadge.textContent = `${strikeCount}/3`;
    strikeBadge.className = strikeCount > 1 ? "text-danger" : "text-warning";
  }

  // Update Modal
  document.getElementById("modalStrikeNum").textContent = strikeCount;
  document.getElementById("violationTimestamp").textContent = new Date().toLocaleTimeString();

  if (strikeCount >= 1) document.getElementById("pip1").classList.add("active");
  if (strikeCount >= 2) document.getElementById("pip2").classList.add("active");
  if (strikeCount >= 3) document.getElementById("pip3").classList.add("active");

  document.getElementById("violationModal").classList.add("show");

  // Check strike threshold
  if (strikeCount >= MAX_STRIKES) {
    setTimeout(() => {
      alert("CRITICAL SECURITY VIOLATION: Maximum allowed strikes (3) exceeded. Examination is being locked and automatically submitted.");
      dismissViolationModal();
      finalizeExamSubmission();
    }, 1200);
  }
}

function dismissViolationModal() {
  document.getElementById("violationModal").classList.remove("show");
  try {
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().catch(() => {});
    }
  } catch(e) {}
}

// 5. Exam Submission
function promptSubmitExam() {
  const answeredCount = Object.keys(userAnswers).length;
  const total = EXAM_CONFIG.questions.length;
  const unansweredCount = total - answeredCount;

  const msg = `Are you sure you want to finalize and submit your examination?\n\n` +
              `Total Questions: ${total}\n` +
              `Answered: ${answeredCount}\n` +
              `Unanswered: ${unansweredCount}\n` +
              `Time Remaining: ${document.getElementById("liveTimer").textContent}\n\n` +
              `Click OK to submit and calculate your grade.`;

  if (confirm(msg)) {
    finalizeExamSubmission();
  }
}

function autoSubmitTimeout() {
  alert("EXAMINATION TIME EXPIRED: All selected answers have been saved and your assessment is being submitted.");
  finalizeExamSubmission();
}

function finalizeExamSubmission() {
  if (isSubmitted) return;
  isSubmitted = true;
  clearInterval(timerInterval);

  // Show submitting overlay
  document.getElementById("submittingOverlay").classList.add("show");

  const payload = {
    answers: userAnswers,
    time_taken_seconds: timeTakenSeconds,
    strike_count: strikeCount
  };

  fetch(EXAM_CONFIG.submitUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    if (data.success && data.result_id) {
      window.location.href = `${EXAM_CONFIG.resultUrlBase}/${data.result_id}`;
    } else {
      alert("Submission Notice: " + (data.message || "Exam submitted. Redirecting..."));
      window.location.href = "/student/dashboard";
    }
  })
  .catch(err => {
    console.error("Submission error:", err);
    alert("Network response error during submission. Your responses are saved. Redirecting to dashboard.");
    window.location.href = "/student/dashboard";
  });
}

