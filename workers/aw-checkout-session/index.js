/**
 * Cloudflare Worker: creates Stripe Checkout Sessions (REST API, no Stripe SDK bundle).
 *
 * Secrets: STRIPE_SECRET_KEY
 * Vars (optional): ALLOWED_ORIGINS — comma-separated
 *
 * POST /create-session
 * Body: { price_id, success_url, cancel_url }
 */
const DEFAULT_ORIGINS = [
  "https://authenticwellness.com",
  "https://www.authenticwellness.com",
  "http://localhost:8788",
  "http://127.0.0.1:8788",
];

function corsHeaders(origin, env) {
  const extra = (env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  const allowed = new Set([...DEFAULT_ORIGINS, ...extra]);
  const o = origin && allowed.has(origin) ? origin : DEFAULT_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": o,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    Vary: "Origin",
  };
}

async function stripeGet(secret, path) {
  const res = await fetch(`https://api.stripe.com${path}`, {
    headers: { Authorization: `Bearer ${secret}` },
  });
  return res.json();
}

async function stripePostForm(secret, path, params) {
  const body = new URLSearchParams(params);
  const res = await fetch(`https://api.stripe.com${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${secret}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });
  return res.json();
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const c = corsHeaders(origin, env);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: c });
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405, headers: c });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return Response.json({ error: "Invalid JSON" }, { status: 400, headers: c });
    }

    const { price_id, success_url, cancel_url } = body;
    if (!price_id || !success_url || !cancel_url) {
      return Response.json(
        { error: "price_id, success_url, and cancel_url are required" },
        { status: 400, headers: c },
      );
    }

    if (!/^price_[a-zA-Z0-9]+$/.test(price_id)) {
      return Response.json({ error: "Invalid price_id" }, { status: 400, headers: c });
    }

    const secret = env.STRIPE_SECRET_KEY;
    if (!secret) {
      return Response.json({ error: "Worker missing STRIPE_SECRET_KEY" }, { status: 500, headers: c });
    }

    const price = await stripeGet(secret, `/v1/prices/${encodeURIComponent(price_id)}`);
    if (price.error) {
      return Response.json({ error: price.error.message || "Invalid price" }, { status: 400, headers: c });
    }

    const mode = price.type === "one_time" ? "payment" : "subscription";

    const session = await stripePostForm(secret, "/v1/checkout/sessions", {
      mode,
      success_url,
      cancel_url,
      client_reference_id: "authentic_wellness",
      "metadata[source]": "authentic_wellness_static",
      "line_items[0][price]": price_id,
      "line_items[0][quantity]": "1",
    });

    if (session.error) {
      return Response.json({ error: session.error.message }, { status: 502, headers: c });
    }
    return Response.json({ url: session.url }, { headers: c });
  },
};
