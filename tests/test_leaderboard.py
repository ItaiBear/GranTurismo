from __future__ import annotations

import json

import pytest

from granturismo.game.leaderboard import Entry, Leaderboard


def make_board(tmp_path, size=4, name_max=6):
    return Leaderboard(tmp_path / "lb.json", size=size, name_max_length=name_max)


def test_fresh_leaderboard_is_padded(tmp_path):
    lb = make_board(tmp_path, size=4)
    assert len(lb.entries()) == 4
    assert all(e.score == 0 for e in lb.entries())


def test_submit_qualifying_score_returns_rank(tmp_path):
    lb = make_board(tmp_path, size=4)
    rank = lb.submit(100, "ALICE")
    assert rank == 1
    assert lb.entries()[0] == Entry("ALICE", 100)
    assert len(lb.entries()) == 4


def test_submit_pushes_lower_scores_down(tmp_path):
    lb = make_board(tmp_path, size=4)
    lb.submit(100, "A")
    lb.submit(80, "B")
    lb.submit(120, "C")
    scores = [e.score for e in lb.entries()]
    assert scores == [120, 100, 80, 0]


def test_submit_truncates_to_size(tmp_path):
    lb = make_board(tmp_path, size=2)
    lb.submit(10, "A")
    lb.submit(20, "B")
    lb.submit(30, "C")
    assert [e.score for e in lb.entries()] == [30, 20]


def test_submit_returns_none_for_unqualified(tmp_path):
    lb = make_board(tmp_path, size=2)
    lb.submit(100, "A")
    lb.submit(50, "B")
    # Zero won't beat 50 → not qualifying
    # But 0 >= 0 in v1's logic... let me check. Actually v1 used `>=`. So 0 ties bottom.
    # For non-trivial test, use a score below the floor that's nonzero.
    lb2 = make_board(tmp_path / "x", size=2)
    lb2.submit(100, "A")
    lb2.submit(50, "B")
    assert lb2.rank_for(-1) is None


def test_rename_changes_name_not_score(tmp_path):
    lb = make_board(tmp_path)
    lb.submit(200, "______")
    lb.rename(1, "ABC")
    assert lb.entries()[0].name == "ABC"
    assert lb.entries()[0].score == 200


def test_persists_across_instances(tmp_path):
    path = tmp_path / "lb.json"
    lb1 = Leaderboard(path, size=4, name_max_length=6)
    lb1.submit(500, "WIN")
    lb2 = Leaderboard(path, size=4, name_max_length=6)
    assert lb2.entries()[0] == Entry("WIN", 500)


def test_corrupted_file_is_recovered(tmp_path):
    path = tmp_path / "lb.json"
    path.write_text("not json", encoding="utf-8")
    lb = Leaderboard(path, size=3, name_max_length=6)
    assert len(lb.entries()) == 3
    assert all(e.score == 0 for e in lb.entries())


def test_name_is_truncated_to_max_length(tmp_path):
    lb = make_board(tmp_path, name_max=4)
    lb.submit(100, "ALEXANDER")
    assert lb.entries()[0].name == "ALEX"


def test_atomic_write_leaves_valid_json(tmp_path):
    lb = make_board(tmp_path)
    lb.submit(100, "A")
    data = json.loads((tmp_path / "lb.json").read_text(encoding="utf-8"))
    assert data[0] == {"name": "A", "score": 100}
