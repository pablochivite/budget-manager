# AI disclosure

Tool: Claude (Anthropic), through Claude Code.

What the AI produced:
- A step-by-step plan for the practice, based on the professor's brief.
- The code in models.py, validation.py, services.py, storage.py and cli.py,
  plus the sample data and the tests. I typed or pasted each file myself, ran
  every command and compared the output with what I expected.
- After a review, two fixes: amounts such as "inf" and "nan" are now rejected,
  and add/undo no longer rewrite a file that has invalid rows (which used to
  delete those rows). It also wrote the tests for both fixes.
- The paragraph in DESIGN.md, which I read and checked against the code.

Why I used it: I had never built a layered, tested project before and wanted
to see how one fits together.

What I checked and can explain:
- Validation lives in one place: make_transaction checks both typed input and
  CSV rows, so the two paths can never apply different rules.
- Unknown categories, kinds and currencies are rejected, not guessed, and each
  error says which row and field failed.
- Undo saves the file straight away, so after a crash and reload the file still
  matches what the program showed.
