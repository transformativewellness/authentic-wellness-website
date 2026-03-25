const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
    navToggle.classList.toggle("active");
  });
}

function closeAllNavDropdowns() {
  document.querySelectorAll(".nav-dropdown").forEach((dd) => {
    dd.classList.remove("open");
    const btn = dd.querySelector(".nav-dropdown-toggle");
    if (btn) btn.setAttribute("aria-expanded", "false");
  });
}

document.querySelectorAll(".nav-dropdown-toggle").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    const wrap = btn.closest(".nav-dropdown");
    if (!wrap) return;
    const willOpen = !wrap.classList.contains("open");
    closeAllNavDropdowns();
    if (willOpen) {
      wrap.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
    }
  });
});

document.addEventListener("click", () => {
  closeAllNavDropdowns();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeAllNavDropdowns();
});

document.querySelectorAll(".nav-dropdown-menu").forEach((menu) => {
  menu.addEventListener("click", (e) => e.stopPropagation());
});

document.querySelectorAll(".faq-question").forEach((button) => {
  button.addEventListener("click", () => {
    const item = button.parentElement;
    const isOpen = item.classList.contains("open");
    document.querySelectorAll(".faq-item").forEach((faq) => faq.classList.remove("open"));
    if (!isOpen) item.classList.add("open");
  });
});

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

window.addEventListener("load", () => {
  document.body.classList.add("page-loaded");
});

const cookieBanner = document.getElementById("cookie-banner");
const cookieDismiss = document.getElementById("cookie-dismiss");
if (cookieBanner && cookieDismiss) {
  const cookieAccepted = localStorage.getItem("aw_cookie_consent");
  if (!cookieAccepted) cookieBanner.classList.add("show");
  cookieDismiss.addEventListener("click", () => {
    localStorage.setItem("aw_cookie_consent", "accepted");
    cookieBanner.classList.remove("show");
  });
}
