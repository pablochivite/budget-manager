# Personal Budget Manager (Release 1)

A command-line budget manager. It records income and expenses in a CSV file,
checks every value before it is saved, and shows a summary per category.

## Setup
Needs uv (https://docs.astral.sh/uv/).

    git clone https://github.com/pablochivite/budget-manager.git
    cd budget-manager
    uv sync

## Run
    uv run budget --help
    uv run budget add 1500 --kind income --category salary --date 2026-09-01
    uv run budget add 18.50 --category food --date 2026-09-04
    uv run budget list
    uv run budget list --category food
    uv run budget summary
    uv run budget undo

Data is saved in data/transactions.csv (created on the first add).

## Example
    $ uv run budget add -5 --category food
    error: amount must be > 0, got -5          (exit code 2, nothing saved)

## Sample data
data/sample_transactions.csv has 5 valid rows and 4 invalid ones
(negative amount, unknown category, 31 September, amount 0):

    uv run budget --file data/sample_transactions.csv summary

Each invalid row is reported as "Row N: ..." and skipped by list and summary.
add and undo refuse to change a file that has invalid rows (exit code 2,
nothing saved), because rewriting it would delete those rows.

## Test
    uv run pytest -v

## Known limitations
- One currency only (EUR).
- Amounts are floats rounded to 2 decimals; a real money app would use Decimal.
- Undo removes only the last transaction; there is no redo.
- No editing of an existing transaction.