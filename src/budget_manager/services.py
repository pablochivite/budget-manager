"""The budget logic: add, filter, summarize, undo. Data in, data out: no input(), no files."""

from budget_manager.models import Transaction
from budget_manager.validation import make_transaction


def next_id(transactions: list[Transaction]) -> str:
    """T001, T002, ... one more than the highest id so far."""
    numbers = [int(t.id[1:]) for t in transactions if t.id[1:].isdigit()]
    return f"T{max(numbers, default=0) + 1:03d}"


def add(
    transactions: list[Transaction],
    amount: str,
    kind: str,
    category: str,
    day: str,
    currency: str = "EUR",
) -> list[Transaction]:
    """Return a new list with the new transaction at the end. Raises ValueError if invalid."""
    row = {
        "id": next_id(transactions),
        "date": day,
        "kind": kind,
        "category": category,
        "amount": amount,
        "currency": currency,
    }
    return [*transactions, make_transaction(row)]


def filter_by(
    transactions: list[Transaction], kind: str | None = None, category: str | None = None
) -> list[Transaction]:
    """Only the transactions that match the given kind and/or category."""
    return [
        t
        for t in transactions
        if (kind is None or t.kind == kind) and (category is None or t.category == category)
    ]


def summarize(transactions: list[Transaction]) -> dict:
    """Totals: income, expenses, balance, and expenses per category (largest first)."""
    income = sum(t.amount for t in transactions if t.kind == "income")
    expenses = sum(t.amount for t in transactions if t.kind == "expense")
    by_category: dict[str, float] = {}
    for t in transactions:
        if t.kind == "expense":
            by_category[t.category] = by_category.get(t.category, 0) + t.amount
    ordered = dict(sorted(by_category.items(), key=lambda item: item[1], reverse=True))
    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "by_category": {c: round(v, 2) for c, v in ordered.items()},
    }


def undo_last(transactions: list[Transaction]) -> tuple[list[Transaction], Transaction]:
    """Remove the last transaction. Raises ValueError when there is nothing to undo."""
    if not transactions:
        raise ValueError("nothing to undo: there are no transactions")
    return transactions[:-1], transactions[-1]