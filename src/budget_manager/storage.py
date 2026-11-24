"""Reading and writing the CSV file. No rules and no printing here."""

import csv
from dataclasses import asdict
from pathlib import Path

from budget_manager.models import FIELDS, Transaction
from budget_manager.validation import make_transaction


def load(path: Path) -> tuple[list[Transaction], list[str]]:
    """Read every row. Returns the valid transactions and one error message per bad row."""
    if not path.exists():
        return [], []
    transactions: list[Transaction] = []
    errors: list[str] = []
    with open(path, newline="", encoding="utf-8") as f:
        # start=2: row 1 of the file is the header
        for number, row in enumerate(csv.DictReader(f), start=2):
            try:
                transactions.append(make_transaction(row))
            except (ValueError, KeyError) as error:
                errors.append(f"Row {number}: {error}")
    return transactions, errors


def save(path: Path, transactions: list[Transaction]) -> None:
    """Write all transactions. A temporary file first, so a crash never leaves half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    with open(temporary, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for t in transactions:
            row = asdict(t)
            row["amount"] = f"{t.amount:.2f}"  # always two decimals in the file
            writer.writerow(row)
    temporary.replace(path)