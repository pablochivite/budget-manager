"""The command line: read the arguments, call storage and services, print. No rules here."""

import argparse
import sys
from datetime import date
from pathlib import Path

from budget_manager import services, storage
from budget_manager.models import CATEGORIES, KINDS

DEFAULT_FILE = Path("data/transactions.csv")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="budget", description="Personal budget manager.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="the CSV file to use")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="record one transaction")
    add.add_argument("amount", help="a number greater than 0, for example 18.50")
    add.add_argument("--kind", default="expense", help=f"one of: {', '.join(KINDS)}")
    add.add_argument("--category", required=True, help=f"one of: {', '.join(CATEGORIES)}")
    add.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD (default: today)")

    show = commands.add_parser("list", help="show transactions")
    show.add_argument("--kind")
    show.add_argument("--category")

    commands.add_parser("summary", help="income, expenses, balance and spending per category")
    commands.add_parser("undo", help="remove the last transaction from the file")
    return parser


def print_table(transactions) -> None:
    for t in transactions:
        print(f"{t.id}  {t.date}  {t.kind:<7}  {t.category:<13} {t.amount:>9.2f} {t.currency}")


def print_summary(result: dict) -> None:
    print(f"Income    {result['income']:>10.2f}")
    print(f"Expenses  {result['expenses']:>10.2f}")
    print(f"Balance   {result['balance']:>10.2f}")
    for category, total in result["by_category"].items():
        print(f"  {category:<13} {total:>10.2f}")


def main() -> None:
    args = make_parser().parse_args()
    transactions, errors = storage.load(args.file)
    for message in errors:
        print(f"warning: {args.file}: {message} (row skipped)", file=sys.stderr)

    try:
        if args.command in ("add", "undo") and errors:
            # Saving would rewrite the file without the skipped rows and lose them.
            raise ValueError(
                f"{args.file} has {len(errors)} invalid rows; fix them first (nothing saved)"
            )
        if args.command == "add":
            transactions = services.add(
                transactions, args.amount, args.kind, args.category, args.date
            )
            storage.save(args.file, transactions)
            print(f"Added {transactions[-1].id}")
        elif args.command == "list":
            print_table(services.filter_by(transactions, args.kind, args.category))
        elif args.command == "summary":
            print_summary(services.summarize(transactions))
        elif args.command == "undo":
            transactions, removed = services.undo_last(transactions)
            storage.save(args.file, transactions)
            print(f"Removed {removed.id}")
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()