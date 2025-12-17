# miniagent/tools.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional
import math
import requests

@dataclass
class ToolResult:
    ok: bool
    tool_name: str
    output: str
    meta: Dict[str, Any]

def calculator(expression: str) -> ToolResult:
    """
    Safe-ish calculator: supports numbers and basic operators.
    Disallows builtins, attribute access, etc.
    """
    allowed = "0123456789+-*/(). eE"
    for ch in expression:
        if ch not in allowed:
            return ToolResult(False, "calculator", f"Disallowed character: {ch}", {"expression": expression})

    try:
        # Limit globals/locals
        value = eval(expression, {"__builtins__": {}}, {"math": math})
        return ToolResult(True, "calculator", str(value), {"expression": expression})
    except Exception as e:
        return ToolResult(False, "calculator", f"Error: {e}", {"expression": expression})

def lookup_notes(query: str, path: str = "data/notes.txt", max_lines: int = 12) -> ToolResult:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        hits = []
        q = query.strip().lower()
        for i, line in enumerate(lines):
            if q in line.lower():
                hits.append((i + 1, line.strip()))

        if not hits:
            return ToolResult(True, "lookup_notes", "No matches found.", {"query": query, "path": path})

        preview = hits[:max_lines]
        formatted = "\n".join([f"Line {ln}: {txt}" for ln, txt in preview])
        return ToolResult(True, "lookup_notes", formatted, {"query": query, "path": path, "hits": len(hits)})
    except Exception as e:
        return ToolResult(False, "lookup_notes", f"Error: {e}", {"query": query, "path": path})

def fetch_url(url: str, timeout_s: int = 8) -> ToolResult:
    """
    Minimal URL fetcher for plain text pages. For tonight, we keep it simple.
    """
    try:
        r = requests.get(url, timeout=timeout_s, headers={"User-Agent": "MiniAgent/1.0"})
        content_type = r.headers.get("content-type", "")
        text = r.text[:3000]  # cap
        return ToolResult(True, "fetch_url", text, {"url": url, "status": r.status_code, "content_type": content_type})
    except Exception as e:
        return ToolResult(False, "fetch_url", f"Error: {e}", {"url": url})