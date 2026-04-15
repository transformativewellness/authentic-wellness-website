/**
 * Public Stripe price map for static checkout (price IDs are safe to expose).
 * Regenerate: npm run generate-stripe-config
 * After deploy, set createSessionEndpoint to your Worker URL (see workers/aw-checkout-session).
 */
window.AW_STRIPE_PUBLIC = {
  publishableKey: "",
  /** POST JSON { price_id, success_url, cancel_url } → { url } */
  createSessionEndpoint: "",
  prices: {
  "semaglutide-starter": {
    "monthly": null,
    "quarterly": null
  },
  "semaglutide-standard": {
    "monthly": null,
    "quarterly": null
  },
  "semaglutide-maintenance": {
    "monthly": null,
    "quarterly": null
  },
  "tirzepatide-starter": {
    "monthly": null,
    "quarterly": null
  },
  "tirzepatide-standard": {
    "monthly": null,
    "quarterly": null
  },
  "tirzepatide-maintenance": {
    "monthly": null,
    "quarterly": null
  },
  "semaglutide-oral": {
    "monthly": null,
    "quarterly": null
  },
  "tirzepatide-oral": {
    "monthly": null,
    "quarterly": null
  },
  "semaglutide-drops": {
    "monthly": null,
    "quarterly": null
  },
  "tirzepatide-drops": {
    "monthly": null,
    "quarterly": null
  },
  "stella-weight-loss-combo": {
    "monthly": null,
    "quarterly": null
  },
  "metformin": {
    "monthly": null,
    "quarterly": null
  },
  "ldn": {
    "monthly": null,
    "quarterly": null
  },
  "cjc-ipamorelin": {
    "monthly": null,
    "quarterly": null
  },
  "sermorelin-injectable": {
    "monthly": null,
    "quarterly": null
  },
  "sermorelin-nasal-spray": {
    "monthly": null,
    "quarterly": null
  },
  "tesamorelin": {
    "monthly": null,
    "quarterly": null
  },
  "nad-injectable": {
    "monthly": null,
    "quarterly": null
  },
  "nad-nasal-spray": {
    "monthly": null,
    "quarterly": null
  },
  "epithalon": {
    "monthly": null,
    "quarterly": null
  },
  "mots-c": {
    "monthly": null,
    "quarterly": null
  },
  "ss-31": {
    "monthly": null,
    "quarterly": null
  },
  "thymosin-alpha-1": {
    "monthly": null,
    "quarterly": null
  },
  "ghk-cu": {
    "monthly": null,
    "quarterly": null
  },
  "bpc-157": {
    "monthly": null,
    "quarterly": null
  },
  "bpc-tb-recovery-stack": {
    "monthly": null,
    "quarterly": null
  },
  "semax": {
    "monthly": null,
    "quarterly": null
  },
  "selank": {
    "monthly": null,
    "quarterly": null
  },
  "cognitive-stack": {
    "monthly": null,
    "quarterly": null
  },
  "methylene-blue": {
    "monthly": null,
    "quarterly": null
  },
  "pt-141": {
    "monthly": null,
    "quarterly": null
  },
  "tadalafil-daily": {
    "monthly": null,
    "quarterly": null
  },
  "sildenafil": {
    "monthly": null,
    "quarterly": null
  },
  "mens-hair-loss-oral": {
    "monthly": null,
    "quarterly": null
  },
  "mens-hair-loss-topical": {
    "monthly": null,
    "quarterly": null
  },
  "womens-hair-loss": {
    "monthly": null,
    "quarterly": null
  },
  "discovery-consultation": {
    "oneTime": null
  }
},
};
