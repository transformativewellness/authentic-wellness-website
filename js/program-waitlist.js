/**
 * PDP waitlist: name + email + program slug. Supabase REST when configured; else localStorage queue (key aw_program_waitlist_local).
 */
(function () {
  var STORAGE_KEY = "aw_program_waitlist_local";

  function getProgramSlug(form) {
    var hidden = form.querySelector('input[name="program_slug"]');
    if (hidden && hidden.value) return hidden.value.trim();
    return (document.body.getAttribute("data-aw-product-slug") || "").trim();
  }

  function showStatus(el, msg, isError) {
    if (!el) return;
    el.hidden = !msg;
    el.textContent = msg || "";
    el.classList.toggle("form-status-error", !!isError);
  }

  function saveLocal(payload) {
    try {
      var prev = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      if (!Array.isArray(prev)) prev = [];
      prev.push(payload);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(prev));
    } catch (e) {
      console.warn("[AW waitlist] localStorage save failed", e);
    }
  }

  async function saveSupabase(cfg, row) {
    var url = (cfg.supabaseUrl || "").replace(/\/$/, "");
    var key = cfg.supabaseAnonKey || "";
    var table = cfg.tableName || "program_enrollment_waitlist";
    if (!url || !key) return false;

    var res = await fetch(url + "/rest/v1/" + encodeURIComponent(table), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        apikey: key,
        Authorization: "Bearer " + key,
        Prefer: "return=minimal",
      },
      body: JSON.stringify({
        full_name: row.full_name,
        email: row.email,
        program_slug: row.program_slug,
      }),
    });
    return res.ok;
  }

  function bindPage() {
    var panel = document.getElementById("aw-program-waitlist");
    var form = document.getElementById("aw-program-waitlist-form");
    var thanks = document.getElementById("aw-program-waitlist-thanks");
    var statusEl = document.getElementById("aw-waitlist-status");
    if (!panel || !form || !thanks) return;

    document.querySelectorAll("[data-aw-waitlist-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        panel.hidden = false;
        thanks.hidden = true;
        form.hidden = false;
        panel.scrollIntoView({ behavior: "smooth", block: "start" });
        var first = form.querySelector("input:not([type=hidden])");
        if (first) first.focus();
      });
    });

    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      showStatus(statusEl, "", false);

      var fd = new FormData(form);
      var name = (fd.get("full_name") || "").toString().trim();
      var email = (fd.get("email") || "").toString().trim();
      var programSlug = (fd.get("program_slug") || getProgramSlug(form)).trim();

      if (!name || !email || !programSlug) {
        showStatus(statusEl, "Please fill in all fields.", true);
        return;
      }

      var cfg = window.AW_PROGRAM_WAITLIST || {};
      var payload = {
        full_name: name,
        email: email,
        program_slug: programSlug,
        saved_at: new Date().toISOString(),
        source: "pdp_waitlist",
      };

      try {
        var okRemote = await saveSupabase(cfg, {
          full_name: name,
          email: email,
          program_slug: programSlug,
        });
        if (!okRemote) saveLocal(payload);
      } catch (err) {
        console.warn("[AW waitlist] remote save failed, using localStorage", err);
        saveLocal(payload);
      }

      form.hidden = true;
      thanks.hidden = false;
      thanks.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindPage);
  } else {
    bindPage();
  }
})();
