# miniagent/agent.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional

from .memory import AgentTrace
from .tools import calculator, lookup_notes, fetch_url, ToolResult

@dataclass
class Plan:
    intent: str
    tool_args: Dict[str, Any]
    brief_plan: str

class MiniAgent:
    """
    Deterministic agent planner for tonight:
    - classify intent
    - call tool if needed
    - return final response with trace
    """

    def plan(self, task: str, trace: AgentTrace) -> Plan:
        t = task.strip().lower()

        # very simple heuristics to be reliable and demoable
        if any(k in t for k in ["calculate", "compute", "what is", "evaluate"]) and any(ch.isdigit() for ch in t):
            # try to extract expression by taking everything after "calculate" if present
            expr = task
            for key in ["calculate", "compute", "evaluate"]:
                if key in t:
                    idx = t.find(key)
                    expr = task[idx + len(key):].strip(" :")
            trace.add("planned", intent="calculate", expression=expr)
            return Plan(intent="calculate", tool_args={"expression": expr}, brief_plan="Use calculator tool and return the result.")

        if "notes" in t or "in my notes" in t or "lookup" in t:
            # use the last noun-ish chunk as query fallback
            query = (
                task.lower()
                .replace("lookup", "")
                .replace("notes", "")
                .replace(":", "")
                .strip()
            ) or task

            trace.add("planned", intent="lookup_notes", query=query)
            return Plan(intent="lookup_notes", tool_args={"query": query}, brief_plan="Search local notes file and return matches.")

        if "http://" in t or "https://" in t or "fetch" in t:
            # find first url token
            url = None
            for token in task.split():
                if token.startswith("http://") or token.startswith("https://"):
                    url = token
                    break
            url = url or task
            trace.add("planned", intent="fetch_url", url=url)
            return Plan(intent="fetch_url", tool_args={"url": url}, brief_plan="Fetch URL content and summarize key parts.")

        trace.add("planned", intent="direct")
        return Plan(intent="direct", tool_args={}, brief_plan="Answer directly without tools.")

    def act(self, plan: Plan, trace: AgentTrace) -> Optional[ToolResult]:
        if plan.intent == "calculate":
            res = calculator(**plan.tool_args)
            trace.add("tool_called", tool="calculator", args=plan.tool_args, ok=res.ok)
            trace.add("tool_output", tool="calculator", output=res.output)
            return res

        if plan.intent == "lookup_notes":
            res = lookup_notes(**plan.tool_args)
            trace.add("tool_called", tool="lookup_notes", args=plan.tool_args, ok=res.ok)
            trace.add("tool_output", tool="lookup_notes", output=res.output)
            return res

        if plan.intent == "fetch_url":
            res = fetch_url(**plan.tool_args)
            trace.add("tool_called", tool="fetch_url", args=plan.tool_args, ok=res.ok)
            trace.add("tool_output", tool="fetch_url", output=res.output[:500] + ("..." if len(res.output) > 500 else ""))
            return res

        return None

    def finalize(self, task: str, plan: Plan, tool_result: Optional[ToolResult], trace: AgentTrace) -> str:
        if plan.intent == "direct":
            return f"Final: {task.strip()}"

        if tool_result is None:
            return "Final: No tool was executed."

        if not tool_result.ok:
            return f"Final: Tool `{tool_result.tool_name}` failed. {tool_result.output}"

        if plan.intent == "calculate":
            return f"Final: The result is {tool_result.output} (computed from: {tool_result.meta.get('expression')})."

        if plan.intent == "lookup_notes":
            return "Final: Here are the most relevant note matches:\n" + tool_result.output

        if plan.intent == "fetch_url":
            return "Final: Fetched page content (preview). Next step is to parse and summarize specific sections.\n" + tool_result.output[:800]

        return "Final: Done."

    def run(self, task: str) -> Dict[str, Any]:
        trace = AgentTrace()
        trace.add("received_task", task=task)

        plan = self.plan(task, trace)
        trace.add("plan", intent=plan.intent, tool_args=plan.tool_args, brief_plan=plan.brief_plan)

        tool_result = self.act(plan, trace)
        final = self.finalize(task, plan, tool_result, trace)

        return {
            "task": task,
            "plan": {"intent": plan.intent, "tool_args": plan.tool_args, "brief_plan": plan.brief_plan},
            "final": final,
            "trace": trace.render(),
        }