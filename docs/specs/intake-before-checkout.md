# Spec: Medical intake before Stripe checkout

**Status:** Specification only — no implementation in this change set.  
**Goal:** Align Authentic Wellness enrollment with common direct-to-consumer telehealth patterns (intake → payment) while preserving the existing post-checkout Qualiphy Good Faith Exam (GFE) as the formal physician review.

---

## Non-negotiable: no auto-disqualification from the intake form

**The intake form collects information only. No patient is rejected or disqualified by the form.** Branching questions may clarify details (e.g. follow-ups on medications or symptoms), but every patient who completes intake may proceed to Stripe checkout when a price is configured for that program. **Clinical decisions happen after GFE completion** — the provider reviews the full record (intake responses plus Qualiphy GFE) and determines appropriateness, prescribing, and fulfillment. Nothing in this spec authorizes client-side or server-side “hard stops” that block checkout based on intake answers alone.

---

## Problem statement

Today, **Get Started** opens **Stripe Checkout** immediately; after payment, `/thank-you.html` orients the patient to the async GFE email. Competitors (Hers, Ro, AgelessRx) collect a **structured medical questionnaire before payment**, which matches consumer expectations for “history first, pay second” and keeps payment aligned with the same visit flow.

This spec does **not** replace Qualiphy GFE. Pre-intake is **data collection before payment**; GFE remains the **legal/clinical review** after checkout exactly as today.

---

## User-facing flow (target)

1. Patient lands on `programs/:program` (existing PDP).
2. **Get Started** → `/intake/:program` (new static or worker-routed page; `:program` maps to a stable slug aligned with `data-aw-product-slug` / Stripe catalog slug).
3. Patient completes **8–12 questions** (category-specific). Progress indicator; no clinical outcome claims; clear copy that a licensed provider will review their information after payment via the GFE.
4. On submit: responses persisted; browser redirects to Stripe Checkout with:
   - Existing price IDs and success/cancel URLs unchanged in spirit.
   - **`client_reference_id`** = opaque intake session id (see Data model).
5. After successful payment: existing **thank-you + Qualiphy GFE** flow unchanged.

---

## Consent, acknowledgments, and medical history (Hers / Ro pattern)

Major DTC prescribers integrate **consent** and **medical history** into a single intake flow rather than isolating legal clicks on a separate page.

- **Hers** and **Ro** typically combine: required checkboxes (telehealth consent, privacy/terms, acknowledgment that the visit is not for emergencies, age/state eligibility where shown) **in the same step** as medical history questions — often at the start or end of the questionnaire, with copy that the patient is authorizing the provider to review their answers.
- **Implementation guidance for AW:** Place at minimum: (1) acknowledgment that the patient is requesting a telehealth evaluation for the selected program; (2) link-out or inline summary to Privacy Policy / Terms; (3) not-for-emergencies disclaimer; (4) optional marketing/consent lines only if already approved for the brand. Medical history blocks (meds, allergies, conditions) should appear in logical order **with** those consents so the patient experiences one coherent flow, not a legal wall followed by a disconnected quiz.

Exact checkbox text requires legal/compliance review before launch.

---

## Route and page: `/intake/:program`

### URL mapping

- `:program` values should match the **canonical product slug** used elsewhere (e.g. `tadalafil-daily`, `semaglutide-starter`, `cognitive-stack`).
- Invalid or unknown slugs → 404 or redirect to `programs.html` (product decision).

### UX requirements

- Mobile-first, accessible (labels, errors, keyboard).
- **Hers-like:** ~10 questions; price may be **de-emphasized** on the intake step (optional A/B: show “from $X/mo” vs hide until after intake — product/legal).
- **Ro-like:** optional **price range** early with “final price at checkout.”
- **AgelessRx-like:** price may remain visible on PDP; intake still **precedes** checkout (20 questions is reference max; we target **8–12**).

### Question bank (by category)

Each program belongs to a **category** (reuse internal taxonomy e.g. weight-loss-glp1, sexual-wellness, cognitive, peptides-*, hair). Intake loads a **template** for that category plus **program-specific add-ons**.

**Universal block (all programs):**

- Age bracket or DOB (as allowed by policy).
- Sex assigned at birth / relevant for prescribing (wording per legal).
- Current medications (free text or structured “yes + list”).
- Allergies (yes/no + details).
- Pregnancy/breastfeeding status where applicable.
- Acknowledgment: compounded meds / telehealth / not emergency care (see Consent section above).

**GLP-1 / weight loss**

- Height/weight or BMI self-report.
- GI history (nausea, pancreatitis history — collect detail for provider review).
- Prior GLP-1 use, diabetes, thyroid history (high level).

**ED / sexual wellness**

- Cardiovascular history (high level).
- Nitrate or other contraindicated medications (collect accurately for provider review).
- Hypotension symptoms, recent cardiac events (informational; no checkout block).

**Peptides / longevity / recovery**

- Cancer history / active malignancy (informational for provider review).
- Autoimmune or immunomodulator context where relevant.

**Hair**

- Pattern description, prior treatments, topical vs oral preference already chosen on PDP.

**Cognitive**

- Psychiatric history, MAOI or other relevant combinations (informational for provider review).

Question text requires **legal/compliance** sign-off before launch.

---

## Data model (Supabase)

**Table (conceptual): `intake_sessions`**

| Column | Type | Notes |
|--------|------|--------|
| `id` | uuid | Primary key; use as `client_reference_id` |
| `created_at` | timestamptz | |
| `program_slug` | text | e.g. `tadalafil-daily` |
| `category` | text | Denormalized for reporting |
| `responses` | jsonb | Full answers; version schema with `schema_version` |
| `user_agent` / `ip_hash` | optional | Fraud/abuse; privacy review |
| `checkout_completed_at` | timestamptz nullable | Backfilled via webhook or thank-you callback |
| `stripe_customer_id` | text nullable | If available post-session |

**Retention:** Align with privacy policy and HIPAA/BAA posture (exact retention TBD).

**Security**

- RLS: inserts only from trusted origin (Worker / service role); no public anon read of PII.
- Do not store payment artifacts in Supabase.

---

## Stripe integration

- **Checkout Session** creation (existing Worker) accepts `client_reference_id` = `intake_sessions.id`.
- Webhook handler (if present) can link `checkout.session.completed` to intake row for analytics and support.
- **No change** to line items, prices, or GFE trigger — only adds correlation.

---

## Qualiphy GFE (explicit non-goals)

- Do **not** move GFE before payment in this phase.
- Do **not** remove or shorten post-payment GFE.
- Intake is **not** a substitute for physician review.

---

## Competitor references (patterns only)

| Vendor | Pattern |
|--------|---------|
| Hers | ~10 questions; consent + history often combined; flow before full price emphasis |
| Ro | Similar funnel; sometimes price range upfront; charge after intake; consents integrated |
| AgelessRx | Price on PDP; large intake before payment |

---

## Implementation phases (future work)

1. Supabase migration + RLS + minimal admin view (internal).
2. Static `/intake/*.html` or Worker-rendered template per category.
3. Worker: validate intake id exists and is “fresh” (e.g. &lt; 24h) before creating Checkout Session.
4. Analytics events (optional).
5. Content/compliance sign-off on questions and consent copy.

---

## Open questions

- Should intake be **required** for all SKUs or phased by category initially?
- Single intake for **multi-SKU** PDPs (e.g. semaglutide tiers) — one session with selected tier stored in `responses` vs. query param?

---

## Document history

- 2026-03-28: Initial spec for review (no production changes).
- 2026-04-16: Removed auto-disqualification; added consent/medical-history section (Hers/Ro); clarified provider review after GFE.
