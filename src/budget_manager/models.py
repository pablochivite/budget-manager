"""What a transaction is. No input, no files, no printing."""

from dataclasses import dataclass

KINDS = ("expense", "income")
CATEGORIES = ("food", "transport", "entertainment", "housing", "salary", "other")
CURRENCIES = ("EUR",)
FIELDS: tuple[str, ...] = ("id", "date", "kind", "category", "amount", "currency")


@dataclass(frozen=True)
class Transaction:
    """One movement of money. The amount is always positive; kind says the direction."""

    id: str
    date: str  # ISO format, for example 2026-09-04
    kind: str  # "expense" or "income"
    category: str  # one of CATEGORIES
    amount: float  # always > 0
    currency: str  # "EUR"