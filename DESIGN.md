# Design rationale

All validation rules live in one module, `validation.py`, and every transaction
is built by one function, `make_transaction`. That same function checks a value
typed in the terminal (`add`) and a row read from the CSV file (`load`), so a
rule such as "amount must be a finite number greater than 0" cannot be enforced
on one path and forgotten on the other. Unknown values are rejected, never
guessed, and each error names the field and the row, for example
`Row 5: amount must be > 0, got -12.00`. The other modules keep to one job each:
`cli.py` reads arguments and prints, `services.py` holds the budget logic with no
files or input, and `storage.py` only reads and writes the CSV, so each part can
be tested on its own. One edge case changed the design: loading skips invalid
rows, but saving rewrites the whole file, so an `add` on a file with bad rows
would silently delete them. `add` and `undo` therefore refuse to write until the
file is fixed, because the file on disk must always hold the true data.
