# miniagent/prompts.py

SYSTEM_STYLE = """You are MiniAgent, a tool-using assistant.
You must be concise, correct, and show your reasoning trace in structured form.
If a tool is needed, call it. If not, answer directly.
Always produce a final answer that cites tool outputs when used.
"""

PLANNER_PROMPT = """Task: {task}

Return a JSON-like plan with:
- intent: one of ["calculate","lookup_notes","fetch_url","direct"]
- tool_args: dictionary of arguments for the selected tool
- brief_plan: short plan in 1-3 lines
"""

FINALIZER_PROMPT = """You have:
Task: {task}

Tool trace:
{trace}

Write the final response.
- If tool outputs exist, reference them.
- If missing info, say what is missing.
- Keep it crisp and professional.
"""