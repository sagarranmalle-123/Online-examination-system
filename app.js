// ==========================================
// Online Examination System - Frontend Logic
// Presidency University (CSE2271 Mini Project)
// ==========================================

// Global State
let currentModule = 1;
let currentQuestionIndex = 7; // Question 8 (0-indexed)
let strikeCount = 0;
let maxStrikes = 3;
let timerSeconds = 42 * 60 + 18; // 42 mins 18 secs

// Sample Questions Bank
const questionsData = [
  {
    num: 1,
    stem: "Which of the following UML diagrams represents the static structure of a system by showing classes, attributes, operations, and relationships?",
    options: ["A. Class Diagram", "B. Sequence Diagram", "C. Activity Diagram", "D. Use Case Diagram"],
    correct: "A",
    selected: "A",
    status: "answered"
  },
  {
    num: 2,
    stem: "In database management, which ACID property ensures that transactions are executed in isolation without interference from other concurrent operations?",
    options: ["A. Atomicity", "B. Consistency", "C. Isolation", "D. Durability"],
    correct: "C",
    selected: "C",
    status: "answered"
  },
  {
    num: 3,
    stem: "What is the worst-case time complexity of QuickSort when using a naive pivot selection on an already sorted array?",
    options: ["A. O(n log n)", "B. O(n²)", "C. O(n)", "D. O(log n)"],
    correct: "B",
    selected: "A", // wrong selected
    status: "answered"
  },
  {
    num: 4,
    stem: "Which design pattern is best suited for creating a single instance of a class across the entire application lifecycle?",
    options: ["A. Factory Method", "B. Observer Pattern", "C. Singleton Pattern", "D. Adapter Pattern"],
    correct: "C",
    selected: "C",
    status: "review"
  },
  {
    num: 5,
    stem: "Which HTTP status code signifies that the client must authenticate themselves to get the requested response?",
    options: ["A. 200 OK", "B. 301 Moved", "C. 401 Unauthorized", "D. 500 Internal Error"],
    correct: "C",
    selected: "C",
    status: "answered"
  },
  {
    num: 6,
    stem: "In symmetric key cryptography, how many secret keys are utilized for encrypting and decrypting data between two parties?",
    options: ["A. One shared secret key", "B. Two separate keys", "C. Three asymmetric keys", "D. Zero keys"],
    correct: "A",
    selected: "A",
    status: "answered"
  },
  {
    num: 7,
    stem: "Which protocol is utilized to securely exchange cryptographic keys and establish an encrypted session in HTTPS?",
    options: ["A. FTP", "B. TLS / SSL Handshake", "C. ICMP", "D. SMTP"],
    correct: "B",
    selected: null,
    status: "unanswered"
  },
  {
    num: 8,
    stem: "Which data structure is primarily utilized to implement Breadth First Search (BFS) in a graph traversal algorithm to discover vertices in shortest-distance order?",
    options: [
      "A.  Stack",
      "B.  Queue (Candidate's Active Selection)",
      "C.  Priority Queue / Min-Heap",
      "D.  Binary Search Tree"
    ],
    correct: "B",
    selected: "B",
    status: "answered"
  }
];

// Fill remaining questions up to 25
for (let i = 9; i <= 25; i++) {
  let status = "gray";
  let sel = null;
  if (i === 9 || i === 15) { status = "unanswered"; }
  else if (i === 13) { status = "review"; sel = "B"; }
  else if (i <= 16) { status = "answered"; sel = "A"; }
  
  questionsData.push({
    num: i,
    stem: `Sample Examination Question #${i}: Evaluate the algorithm complexity and design principles for distributed transaction processing.`,
    options: [`A. Option Alpha for Q${i}`, `B. Option Beta for Q${i}`, `C. Option Gamma for Q${i}`, `D. Option Delta for Q${i}`],
    correct: "B",
    selected: sel,
    status: status
  });
}

// Initialize on DOM Load
document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initTimer();
  renderPalette();
  initTabSwitchListener();
});

// Module Navigation Switcher
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const mod = parseInt(tab.dataset.module);
      switchModule(mod);
    });
  });
}

function switchModule(modId) {
  currentModule = modId;
  document.querySelectorAll(".nav-tab").forEach(tab => {
    tab.classList.toggle("active", parseInt(tab.dataset.module) === modId);
  });
  document.querySelectorAll(".module-pane").forEach(pane => {
    pane.classList.toggle("active", pane.id === `module-${modId}`);
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Live Countdown Timer
function initTimer() {
  const timerElem = document.getElementById("examTimer");
  if (!timerElem) return;

  setInterval(() => {
    if (timerSeconds > 0) {
      timerSeconds--;
      const hrs = Math.floor(timerSeconds / 3600);
      const mins = Math.floor((timerSeconds % 3600) / 60);
      const secs = timerSeconds % 60;
      timerElem.textContent = `${pad(hrs)}:${pad(mins)}:${pad(secs)}`;
    } else {
      autoSubmitExamTimeout();
    }
  }, 1000);
}

function pad(n) {
  return n < 10 ? "0" + n : n;
}

// Render 25 Question Navigation Palette
function renderPalette() {
  const grid = document.getElementById("paletteGrid");
  if (!grid) return;
  grid.innerHTML = "";

  questionsData.forEach((q, idx) => {
    const btn = document.createElement("button");
    btn.className = `palette-btn ${q.status}`;
    if (idx === currentQuestionIndex) {
      btn.classList.add("current");
    }
    btn.textContent = q.num;
    btn.onclick = () => loadQuestion(idx);
    grid.appendChild(btn);
  });
}

// Load Question in Live Console
function loadQuestion(idx) {
  currentQuestionIndex = idx;
  const q = questionsData[idx];
  
  document.getElementById("qCurrentBadge").textContent = `QUESTION ${pad(q.num)} OF 25`;
  document.getElementById("qStemText").textContent = q.stem;

  const container = document.getElementById("qOptionsContainer");
  container.innerHTML = "";

  const letters = ["A", "B", "C", "D"];
  q.options.forEach((opt, oIdx) => {
    const letter = letters[oIdx];
    const isSelected = q.selected === letter;

    const label = document.createElement("label");
    label.className = `option-card ${isSelected ? 'selected' : ''}`;
    label.onclick = () => selectOption(letter);

    label.innerHTML = `
      <input type="radio" name="examOption" value="${letter}" ${isSelected ? 'checked' : ''}>
      <span class="opt-text">${opt}</span>
    `;
    container.appendChild(label);
  });

  renderPalette();
}

function selectOption(letter) {
  const q = questionsData[currentQuestionIndex];
  q.selected = letter;
  q.status = "answered";
  loadQuestion(currentQuestionIndex);
}

function clearOption() {
  const q = questionsData[currentQuestionIndex];
  q.selected = null;
  q.status = "unanswered";
  loadQuestion(currentQuestionIndex);
}

function markForReview() {
  const q = questionsData[currentQuestionIndex];
  q.status = "review";
  nextQuestion();
}

function nextQuestion() {
  if (currentQuestionIndex < questionsData.length - 1) {
    loadQuestion(currentQuestionIndex + 1);
  } else {
    alert("You have reached the final question. You may review your palette or click SUBMIT EXAM.");
  }
}

function prevQuestion() {
  if (currentQuestionIndex > 0) {
    loadQuestion(currentQuestionIndex - 1);
  }
}

// Anti-Cheat & Visibility Listener
function initTabSwitchListener() {
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && currentModule === 3) {
      triggerViolation("Window lost focus - Candidate navigated away from active exam session.");
    }
  });
}

function triggerTestViolation() {
  triggerViolation("Simulated Proctor Violation - External application / tab switch detected.");
}

function triggerViolation(reason) {
  strikeCount++;
  const timeStr = new Date().toLocaleTimeString();

  // Update Strike Text & Pips
  document.getElementById("strikeCountText").textContent = strikeCount;
  if (strikeCount >= 1) document.getElementById("pip1").classList.add("active");
  if (strikeCount >= 2) document.getElementById("pip2").classList.add("active");
  if (strikeCount >= 3) document.getElementById("pip3").classList.add("active");
  document.getElementById("violationTimestamp").textContent = timeStr;

  // Log in Module 4 Audit Feed
  const feed = document.getElementById("proctorLogFeed");
  if (feed) {
    const logItem = document.createElement("div");
    logItem.className = "log-entry danger";
    logItem.innerHTML = `<span class="log-time">${timeStr}</span> <span class="log-msg"><strong>[ALERT]</strong> Strike #${strikeCount} logged for Sagar Ranmalle (20241CSE0750): ${reason}</span>`;
    feed.prepend(logItem);
  }

  // Show Modal Alert
  document.getElementById("violationModal").classList.add("show");

  // If 3 strikes, auto submit!
  if (strikeCount >= maxStrikes) {
    setTimeout(() => {
      alert("CRITICAL VIOLATION: Maximum strike limit (3) exceeded. Exam session is being locked and automatically submitted.");
      document.getElementById("violationModal").classList.remove("show");
      switchModule(5);
    }, 1500);
  }
}

function resumeExamFromModal() {
  document.getElementById("violationModal").classList.remove("show");
  // Try to re-enter fullscreen
  if (document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen().catch(() => {});
  }
}

// Exam Submission Handlers
function confirmSubmitExam() {
  const ansCount = questionsData.filter(q => q.status === "answered").length;
  if (confirm(`Are you sure you want to finalize and submit your examination?\n\nAnswered: ${ansCount} of 25 Questions\nRemaining Time: ${document.getElementById("examTimer").textContent}\n\nClick OK to evaluate.`)) {
    switchModule(5);
  }
}

function autoSubmitExamTimeout() {
  alert("EXAMINATION TIME EXPIRED: All selected answers have been saved and automatically submitted.");
  switchModule(5);
}

