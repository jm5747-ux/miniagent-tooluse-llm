from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Chunk:
    doc_id: str
    chunk_id: int
    text: str


def build_chunks(docs_dir: str, chunk_size: int = 400) -> List[Chunk]:
    chunks: List[Chunk] = []
    base = Path(docs_dir)

    if not base.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    for path in base.glob("*.txt"):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue

        for i in range(0, len(text), chunk_size):
            chunk_text = text[i : i + chunk_size]
            chunks.append(
                Chunk(
                    doc_id=path.name,
                    chunk_id=len(chunks),
                    text=chunk_text,
                )
            )

    return chunks
