/**
 * Forces HTTPS with a 301 so http:// and https:// are not indexed as duplicates.
 * Static files are served via the ASSETS binding (requires run_worker_first in wrangler.toml).
 * Security headers are merged onto every asset response.
 */
const SECURITY_HEADERS = {
  "X-Frame-Options": "SAMEORIGIN",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "Content-Security-Policy": "frame-ancestors 'self'",
};

function withSecurityHeaders(response) {
  const headers = new Headers(response.headers);
  for (const [key, value] of Object.entries(SECURITY_HEADERS)) {
    headers.set(key, value);
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    let insecure = url.protocol === "http:";
    const xf = request.headers.get("X-Forwarded-Proto");
    if (xf === "http") {
      insecure = true;
    }
    const cfVisitor = request.headers.get("CF-Visitor");
    if (cfVisitor) {
      try {
        if (JSON.parse(cfVisitor).scheme === "http") {
          insecure = true;
        }
      } catch {
        /* ignore */
      }
    }

    if (insecure) {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }

    // Redirect removed directory URLs to canonical .html versions
    const redirectMap = {
      "/about/": "/about.html",
      "/contact/": "/contact.html",
      "/privacy-policy/": "/privacy-policy.html",
      "/terms-of-service/": "/terms-of-service.html",
      "/accessibility/": "/accessibility.html",
      "/services/": "/services.html",
    };
    const redirect = redirectMap[url.pathname];
    if (redirect) {
      url.pathname = redirect;
      return Response.redirect(url.toString(), 301);
    }

    const res = await env.ASSETS.fetch(request);
    return withSecurityHeaders(res);
  },
};
