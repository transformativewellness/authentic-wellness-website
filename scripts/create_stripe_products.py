#!/usr/bin/env python3
"""
Create Authentic Wellness catalog Products + Prices in Stripe from stripe-products.json.

Usage (Authentic Wellness Stripe secret key — live or test):
  export STRIPE_SECRET_KEY=sk_live_...   # or sk_test_...
  python3 scripts/create_stripe_products.py

Idempotent: skips products that already have metadata aw_catalog_name set to the same name.

Outputs: prints prod/price IDs; writes scripts/stripe-catalog-ids.json (gitignored).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

try:
    import stripe
except ImportError:
    print("Install Stripe SDK: pip install -r scripts/requirements-stripe.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "stripe-products.json"
OUT_PATH = ROOT / "stripe-catalog-ids.json"
META_KEY = "aw_catalog_name"
META_BRAND = "authentic_wellness"


def load_catalog() -> dict:
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def existing_by_catalog_name() -> dict[str, stripe.Product]:
    """Map aw_catalog_name -> Product (active only)."""
    found: dict[str, stripe.Product] = {}
    for prod in stripe.Product.list(active=True, limit=100).auto_paging_iter():
        name = (prod.metadata or {}).get(META_KEY)
        if name:
            found[name] = prod
    return found


def _price_matches(price: stripe.Price, amount_cents: int, recurring: bool, interval: str | None) -> bool:
    if price.unit_amount != amount_cents or price.currency != "usd":
        return False
    r = price.recurring
    if recurring:
        return r is not None and getattr(r, "interval", None) == interval
    return r is None


def price_exists_for_product(product_id: str, amount_cents: int, recurring: bool, interval: str | None) -> bool:
    for price in stripe.Price.list(product=product_id, active=True, limit=100).auto_paging_iter():
        if _price_matches(price, amount_cents, recurring, interval):
            return True
    return False


def main() -> None:
    key = os.environ.get("STRIPE_SECRET_KEY", "").strip()
    if not key:
        print("Set STRIPE_SECRET_KEY to your Authentic Wellness Stripe secret key (sk_live_... or sk_test_...).", file=sys.stderr)
        sys.exit(1)

    stripe.api_key = key
    data = load_catalog()
    items = data["products"]
    existing = existing_by_catalog_name()

    results: list[dict] = []

    for row in items:
        name = row["name"]
        amount = int(row["amount_cents"])
        recurring = bool(row["recurring"])
        interval = row.get("interval") if recurring else None

        prod = existing.get(name)
        if not prod:
            prod = stripe.Product.create(
                name=name,
                metadata={META_KEY: name, "brand": META_BRAND},
            )
            existing[name] = prod
            print(f"+ product  {prod.id}  {name!r}")
        else:
            print(f"= product  {prod.id}  {name!r} (already exists)")

        if price_exists_for_product(prod.id, amount, recurring, interval):
            pid = None
            for price in stripe.Price.list(product=prod.id, active=True, limit=100).auto_paging_iter():
                if _price_matches(price, amount, recurring, interval):
                    pid = price.id
                    break
            print(f"  = price    {pid} (already exists)")
            results.append({"name": name, "product_id": prod.id, "price_id": pid, "created": False})
            continue

        params: dict = {
            "product": prod.id,
            "unit_amount": amount,
            "currency": "usd",
        }
        if recurring:
            params["recurring"] = {"interval": interval}

        price = stripe.Price.create(**params)
        print(f"  + price    {price.id}  ${amount/100:.2f}  {'/' + interval if recurring else 'one-time'}")
        results.append({"name": name, "product_id": prod.id, "price_id": price.id, "created": True})

    out = {
        "stripe_account_note": data.get("stripe_account", {}),
        "prices": results,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {OUT_PATH} ({len(results)} entries). Use price_id values in GHL / checkout.")


if __name__ == "__main__":
    main()
