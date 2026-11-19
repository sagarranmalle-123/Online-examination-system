// ==========================================
// General Portal UI Helpers
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
  // Auto-dismiss success flash alerts after 5 seconds
  const successAlerts = document.querySelectorAll(".alert-success");
  successAlerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });
});

