"""Run with: uv run pytest -v"""

import pytest

from budget_manager import services, storage
from budget_manager.validation import check_amount


def test_summary_normal_case():
    ts = services.add([], "1000", "income", "salary", "2026-09-01")
    ts = services.add(ts, "18.50", "expense", "food", "2026-09-02")
    ts = services.add(ts, "1.50", "expense", "food", "2026-09-03")
    assert services.summarize(ts) == {
        "income": 1000.0,
        "expenses": 20.0,
        "balance": 980.0,
        "by_category": {"food": 20.0},
    }


@pytest.mark.parametrize("text", ["0", "-5", "abc", "1.005"])
def test_bad_amounts_are_rejected(text):
    with pytest.raises(ValueError):
        check_amount(text)


def test_smallest_amount_is_accepted():
    assert check_amount("0.01") == 0.01


def test_unknown_category_is_rejected():
    with pytest.raises(ValueError, match="category must be one of"):
        services.add([], "10", "expense", "shopping", "2026-09-01")


def test_save_and_load_give_back_the_same(tmp_path):
    ts = services.add([], "18.50", "expense", "food", "2026-09-04")
    path = tmp_path / "t.csv"
    storage.save(path, ts)
    assert storage.load(path) == (ts, [])


def test_undo_is_saved_to_the_file(tmp_path):
    path = tmp_path / "t.csv"
    ts = services.add([], "5", "expense", "food", "2026-09-04")
    ts = services.add(ts, "7", "expense", "food", "2026-09-05")
    ts, removed = services.undo_last(ts)
    storage.save(path, ts)
    assert removed.id == "T002"
    assert storage.load(path)[0] == ts


def test_undo_with_nothing_left_fails():
    with pytest.raises(ValueError, match="nothing to undo"):
        services.undo_last([])


def test_sample_data_reports_each_bad_row():
    from pathlib import Path

    good, errors = storage.load(Path("data/sample_transactions.csv"))
    assert len(good) == 5
    assert [e.split(":")[0] for e in errors] == ["Row 5", "Row 7", "Row 8", "Row 9"]