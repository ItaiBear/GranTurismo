from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable


@dataclass(frozen=True)
class Entry:
    name: str
    score: int

    def to_dict(self) -> dict:
        return {"name": self.name, "score": self.score}


class Leaderboard:
    """JSON-backed top-N leaderboard with atomic writes."""

    def __init__(self, path: str | Path, size: int, name_max_length: int):
        self.path = Path(path)
        self.size = size
        self.name_max_length = name_max_length
        self._entries: list[Entry] = []
        self.load()

    def load(self) -> None:
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                entries = [Entry(e["name"], int(e["score"])) for e in raw]
                self._entries = self._pad(entries)
                return
            except (ValueError, KeyError, TypeError):
                pass
        self.reset()

    def reset(self) -> None:
        self._entries = self._pad([])
        self.save()

    def entries(self) -> list[Entry]:
        return list(self._entries)

    def rank_for(self, score: int) -> int | None:
        """1-based rank a new score would slot into, or None if it doesn't qualify."""
        for i, entry in enumerate(self._entries):
            if score >= entry.score:
                return i + 1
        return None

    def submit(self, score: int, name: str = "______") -> int | None:
        rank = self.rank_for(score)
        if rank is None:
            return None
        new_entry = Entry(self._sanitize_name(name), score)
        self._entries.insert(rank - 1, new_entry)
        self._entries = self._entries[: self.size]
        self.save()
        return rank

    def rename(self, rank: int, name: str) -> None:
        if not 1 <= rank <= len(self._entries):
            return
        current = self._entries[rank - 1]
        self._entries[rank - 1] = Entry(self._sanitize_name(name), current.score)
        self.save()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps([e.to_dict() for e in self._entries], indent=2)
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=self.path.parent, delete=False, suffix=".tmp"
        ) as tmp:
            tmp.write(payload)
            tmp_name = tmp.name
        os.replace(tmp_name, self.path)

    def _pad(self, entries: Iterable[Entry]) -> list[Entry]:
        result = list(entries)[: self.size]
        while len(result) < self.size:
            result.append(Entry("______", 0))
        return result

    def _sanitize_name(self, name: str) -> str:
        # Truncate but allow any unicode (the v1 keyboard-layout English-only
        # restriction is intentionally dropped here).
        return (name or "______")[: self.name_max_length]
