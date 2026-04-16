/**
 * Static site checkout: creates Stripe Checkout Session via Worker (see workers/aw-checkout-session).
 * Requires js/stripe-config.js first (window.AW_STRIPE_PUBLIC).
 *
 * Buttons:
 * - .aw-checkout[data-billing="monthly"|"quarterly"] — uses body[data-aw-product-slug] or data-product-slug
 * - .aw-checkout[data-checkout-one-time="1"] — legacy one-time product slug (e.g. enrollment); requires data-product-slug
 */
(function () {
  /** Map legacy marketing slugs / old PDP keys to current Stripe config keys. */
  const LEGACY_SLUG = {
    perform: "cjc-ipamorelin",
    renew: "sermorelin-injectable",
    recovery: "bpc-157",
    longevity: "nad-injectable",
  };

  function getConfig() {
    return window.AW_STRIPE_PUBLIC;
  }

  function resolveSlug(btn) {
    const explicit = btn.getAttribute("data-product-slug");
    if (explicit) return explicit;
    const body = document.body;
    return body.getAttribute("data-aw-product-slug") || "";
  }

  function normalizeSlug(slug) {
    if (!slug) return slug;
    return LEGACY_SLUG[slug] || slug;
  }

  function getPriceId(slug, billing, oneTime) {
    const cfg = getConfig();
    slug = normalizeSlug(slug);
    if (!cfg || !cfg.prices || !slug) return null;
    const row = cfg.prices[slug];
    if (!row) return null;
    if (oneTime) return row.oneTime || null;
    if (billing === "quarterly") return row.quarterly || null;
    return row.monthly || null;
  }

  async function startCheckout(priceId) {
    const cfg = getConfig();
    const endpoint = cfg && cfg.createSessionEndpoint;
    if (!endpoint) {
      console.warn(
        "[AW checkout] Set AW_STRIPE_PUBLIC.createSessionEndpoint (Worker URL). Checkout cannot start without it.",
      );
      window.location.href = `${window.location.origin}/contact.html?reason=checkout_not_configured`;
      return;
    }
    const origin = window.location.origin;
    const success_url = `${origin}/thank-you.html?session_id={CHECKOUT_SESSION_ID}`;
    const cancel_url = `${origin}/checkout-cancel.html`;

    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ price_id: priceId, success_url, cancel_url }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      console.error("[AW checkout]", data.error || res.status);
      window.location.href = `${window.location.origin}/contact.html?reason=checkout_session_error`;
      return;
    }
    if (data.url) {
      window.location.href = data.url;
    }
  }

  document.addEventListener(
    "click",
    function (e) {
      const btn = e.target.closest(".aw-checkout");
      if (!btn) return;
      e.preventDefault();

      const slug = resolveSlug(btn);
      const oneTime = btn.getAttribute("data-checkout-one-time") === "1";
      const billing = btn.getAttribute("data-billing") || "monthly";

      const priceId = getPriceId(slug, billing, oneTime);
      if (!priceId || String(priceId).startsWith("price_PENDING")) {
        console.warn("[AW checkout] Missing Stripe price id for", slug, billing, oneTime);
        var q = new URLSearchParams({ reason: "no_price", program: slug || "" });
        window.location.href = `${window.location.origin}/contact.html?${q.toString()}`;
        return;
      }

      void startCheckout(priceId);
    },
    true,
  );
})();
