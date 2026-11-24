"""All the rules in one place. Every check raises ValueError with a clear message."""

import math
from datetime import date

from budget_manager.models import CATEGORIES, CURRENCIES, KINDS, Transaction


def check_amount(text: str) -> float:
    """Turn the text into an amount, which must be a number greater than 0."""
    try:
        amount = float(text)
    except ValueError:
        raise ValueError(f"amount must be a number, got {text!r}") from None
    if not math.isfinite(amount):  # float() accepts "inf" and "nan"
        raise ValueError(f"amount must be a finite number, got {text!r}")
    if amount <= 0:
        raise ValueError(f"amount must be > 0, got {text}")
    if round(amount, 2) != amount:
        raise ValueError(f"amount can have at most 2 decimals, got {text}")
    return amount


def check_choice(name: str, value: str, allowed: tuple[str, ...]) -> str:
    """Policy: unknown values are rejected, never guessed or silently fixed."""
    if value not in allowed:
        raise ValueError(f"{name} must be one of {', '.join(allowed)}, got {value!r}")
    return value


def check_date(text: str) -> str:
    """The date must be a real day in ISO format: YYYY-MM-DD."""
    try:
        date.fromisoformat(text)
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD, got {text!r}") from None
    return text


def make_transaction(row: dict[str, str]) -> Transaction:
    """Build a Transaction from text fields (a CSV row or typed input), checking each one."""
    return Transaction(
        id=row["id"],
        date=check_date(row["date"]),
        kind=check_choice("kind", row["kind"], KINDS),
        category=check_choice("category", row["category"], CATEGORIES),
        amount=check_amount(row["amount"]),
        currency=check_choice("currency", row["currency"], CURRENCIES),
    )