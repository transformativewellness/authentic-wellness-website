const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const navInner = document.querySelector(".nav-inner");

let navScrollLockY = 0;

function setMobileNavOpen(open) {
  if (!navLinks || !navToggle) return;
  const wasOpen = navLinks.classList.contains("open");
  navLinks.classList.toggle("open", open);
  navToggle.classList.toggle("active", open);
  navToggle.setAttribute("aria-expanded", open ? "true" : "false");
  document.body.classList.toggle("nav-menu-open", open);
  if (open) {
    navScrollLockY = window.scrollY;
    document.body.style.top = `-${navScrollLockY}px`;
  } else if (wasOpen) {
    document.body.style.top = "";
    window.scrollTo(0, navScrollLockY);
  }
}

if (navToggle && navLinks) {
  navToggle.setAttribute("aria-expanded", "false");
  navToggle.setAttribute("aria-controls", "primary-navigation");

  navToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    setMobileNavOpen(!navLinks.classList.contains("open"));
  });

  navLinks.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", () => setMobileNavOpen(false));
  });

  navLinks.querySelectorAll("button").forEach((btn) => {
    if (btn.classList.contains("nav-dropdown-toggle")) return;
    btn.addEventListener("click", () => {
      window.setTimeout(() => setMobileNavOpen(false), 350);
    });
  });

  document.addEventListener("click", (e) => {
    if (!navLinks.classList.contains("open")) return;
    if (navInner && !navInner.contains(e.target)) {
      setMobileNavOpen(false);
    }
  });

  window.addEventListener("resize", () => {
    if (window.matchMedia("(min-width: 768px)").matches && navLinks.classList.contains("open")) {
      setMobileNavOpen(false);
    }
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
  if (e.key !== "Escape") return;
  if (navLinks?.classList.contains("open")) {
    setMobileNavOpen(false);
  }
  closeAllNavDropdowns();
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
  initMobileStickyCta();
});

/**
 * Fixed bottom CTA on small viewports — keeps primary conversion action one tap away after scroll.
 * Requires Qualiphy's showDisclosureModal (loaded before this runs on window load).
 */
function initMobileStickyCta() {
  const mq = window.matchMedia("(max-width: 767px)");

  function removeBar() {
    document.getElementById("aw-mobile-sticky-cta")?.remove();
    document.body.classList.remove("aw-has-mobile-sticky-cta");
  }

  function mountBar() {
    if (typeof window.showDisclosureModal !== "function") return;
    if (document.getElementById("aw-mobile-sticky-cta")) {
      document.body.classList.add("aw-has-mobile-sticky-cta");
      return;
    }

    const bar = document.createElement("div");
    bar.id = "aw-mobile-sticky-cta";
    bar.className = "aw-mobile-sticky-cta";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Start your program");

    const inner = document.createElement("div");
    inner.className = "aw-mobile-sticky-cta-inner";

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn btn-amber aw-mobile-sticky-cta-btn";
    btn.textContent = "Start my program";
    btn.addEventListener("click", () => {
      if (typeof window.showDisclosureModal === "function") {
        window.showDisclosureModal();
      }
    });

    const micro = document.createElement("p");
    micro.className = "aw-mobile-sticky-cta-micro";
    micro.textContent =
      "Full medication refund if not approved by your physician. Consultation fee is non-refundable.";

    inner.appendChild(btn);
    inner.appendChild(micro);
    bar.appendChild(inner);
    document.body.appendChild(bar);
    document.body.classList.add("aw-has-mobile-sticky-cta");
  }

  function apply() {
    if (!mq.matches) {
      removeBar();
      return;
    }
    mountBar();
  }

  apply();
  mq.addEventListener("change", apply);
}

/** Qualiphy disclosure: inject telehealth consent copy when modal mounts (script is external). */
(function initQualiphyDisclosureEnhancements() {
  const telehealthHtml =
    "By proceeding, you consent to a virtual physician consultation via Qualiphy's secure telehealth platform. A licensed, independent physician will review your health history and determine if treatment is appropriate. Physician approval is required — this is not a guarantee of a prescription. You can access the full <a href=\"/terms.html\">Terms of Service</a> and <a href=\"/privacy.html\">Privacy Policy</a> below.";

  function legalPathPrefix() {
    const seg = window.location.pathname.split("/").filter(Boolean)[0];
    return seg === "programs" || seg === "blog" ? "../" : "";
  }

  function prefixTermsPrivacyLinks(container) {
    const prefix = legalPathPrefix();
    container.querySelectorAll('a[href="/terms.html"], a[href="/privacy.html"]').forEach((a) => {
      const href = a.getAttribute("href");
      if (href === "/terms.html") {
        a.setAttribute("href", `${prefix}terms.html`);
      }
      if (href === "/privacy.html") {
        a.setAttribute("href", `${prefix}privacy.html`);
      }
    });
  }

  function enhanceInnerModel(inner) {
    if (!inner || inner.dataset.awTelehealthEnhanced) return;
    inner.dataset.awTelehealthEnhanced = "1";
    const p = document.createElement("p");
    p.className = "aw-disclosure-telehealth compliance-disclaimer";
    p.innerHTML = telehealthHtml;
    prefixTermsPrivacyLinks(p);
    inner.insertBefore(p, inner.firstChild);
  }

  const obs = new MutationObserver(() => {
    const inner = document.querySelector("#inner-model");
    if (inner) enhanceInnerModel(inner);
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();

const cookieBanner = document.getElementById("cookie-banner");
const cookieDismiss = document.getElementById("cookie-dismiss");
if (cookieBanner && cookieDismiss) {
  const cookieAccepted = localStorage.getItem("aw_cookie_consent");
  if (!cookieAccepted) {
    cookieBanner.classList.add("show");
    document.body.classList.add("aw-cookie-visible");
  }
  cookieDismiss.addEventListener("click", () => {
    localStorage.setItem("aw_cookie_consent", "accepted");
    cookieBanner.classList.remove("show");
    document.body.classList.remove("aw-cookie-visible");
  });
}
