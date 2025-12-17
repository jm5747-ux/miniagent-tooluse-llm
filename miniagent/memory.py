# miniagent/memory.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TraceStep:
    step: str
    detail: Dict[str, Any]

@dataclass
class AgentTrace:
    steps: List[TraceStep] = field(default_factory=list)

    def add(self, step: str, **detail: Any) -> None:
        self.steps.append(TraceStep(step=step, detail=detail))

    def render(self) -> str:
        lines = []
        for i, s in enumerate(self.steps, start=1):
            lines.append(f"{i}. {s.step}: {s.detail}")
        return "\n".join(lines)