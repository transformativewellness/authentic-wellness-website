/**
 * Contact form: Web3Forms when AW_WEB3FORMS_ACCESS_KEY is set, otherwise mailto fallback.
 * Create a key at https://web3forms.com and restrict allowed domains to authenticwellness.com.
 * Spam controls (e.g. reCAPTCHA) can be enabled in the Web3Forms dashboard without embedding site secrets here.
 */
const AW_WEB3FORMS_ACCESS_KEY = "";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("aw-contact-form");
  if (!form) return;

  const statusEl = document.getElementById("aw-contact-status");
  const submitBtn = form.querySelector('button[type="submit"]');

  function setStatus(msg, isError) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.classList.toggle("form-status-error", !!isError);
    statusEl.hidden = !msg;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setStatus("", false);

    const hp = form.querySelector('input[name="botcheck"]');
    if (hp && hp.value.trim()) return;

    const consent = form.querySelector('input[name="consent"]');
    if (!consent || !consent.checked) {
      setStatus("Please confirm you agree to our Privacy Policy before sending.", true);
      consent?.focus();
      return;
    }

    const name = form.querySelector('[name="name"]')?.value.trim() || "";
    const email = form.querySelector('[name="email"]')?.value.trim() || "";
    const phone = form.querySelector('[name="phone"]')?.value.trim() || "";
    const topicEl = form.querySelector('[name="topic"]');
    const topic = topicEl ? topicEl.value.trim() || "General" : "General";
    const message = form.querySelector('[name="message"]')?.value.trim() || "";

    if (name.length < 2) {
      setStatus("Please enter your name.", true);
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setStatus("Please enter a valid email address.", true);
      return;
    }
    if (message.length < 10) {
      setStatus("Please enter a message (at least 10 characters).", true);
      return;
    }
    if (message.length > 5000) {
      setStatus("Message is too long. Please keep it under 5,000 characters.", true);
      return;
    }

    if (AW_WEB3FORMS_ACCESS_KEY) {
      if (submitBtn) submitBtn.disabled = true;
      try {
        const res = await fetch("https://api.web3forms.com/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({
            access_key: AW_WEB3FORMS_ACCESS_KEY,
            subject: `[AW Website] ${topic} — ${name}`,
            name,
            email,
            phone: phone || undefined,
            message: `Topic: ${topic}\n\n${message}`,
            replyto: email,
          }),
        });
        const data = await res.json();
        if (data.success) {
          setStatus("Thank you — your message was sent. We will reply by email.", false);
          form.reset();
        } else {
          setStatus(data.message || "Something went wrong. Please email info@authenticwellness.com.", true);
        }
      } catch {
        setStatus("Network error. Please email info@authenticwellness.com.", true);
      }
      if (submitBtn) submitBtn.disabled = false;
      return;
    }

    const subj = encodeURIComponent(`[AW Website] ${topic} — ${name}`);
    const body = encodeURIComponent(
      `Name: ${name}\nEmail: ${email}\nPhone: ${phone || "(none)"}\nTopic: ${topic}\n\n${message}`
    );
    window.location.href = `mailto:info@authenticwellness.com?subject=${subj}&body=${body}`;
    setStatus(
      "If your email app did not open, copy your message and send it to info@authenticwellness.com.",
      false
    );
  });
});
