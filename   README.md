# MiniAgent: Tool-Using Agentic System (Python)

MiniAgent is a lightweight agentic system that routes tasks through a planner, selects tools, executes actions, and produces a final response with a structured trace.

This project demonstrates practical agentic system engineering: tool selection, execution control flow, and transparent logging for reliability.

## Why this matters
Modern LLM systems increasingly require "agentic" behavior: planning, tool use, and grounded outputs rather than purely free-form generation. This repo provides a clean, testable skeleton for building tool-using AI assistants.

## Features
- Deterministic planning and routing
- Tool execution with traceability
- Tools included:
  - Calculator
  - Local notes lookup (simple retrieval)
  - URL fetch (content preview)

## Architecture Overview

MiniAgent follows a simple, explicit agent loop:

1. A task is received from the CLI
2. The planner decides which tool to use
3. The selected tool is executed with validated inputs
4. Results are logged in a structured trace
5. A final response is returned to the user

This design prioritizes transparency, debuggability, and safe tool usage.

## Quickstart

### 1) Install
python -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt

### 2) Run examples
python -m miniagent.cli --task "calculate (45*3) / 5"  
python -m miniagent.cli --task "lookup notes: hallucinations"  
python -m miniagent.cli --task "fetch https://example.com"

## Repo structure
miniagent/ contains the agent loop, tools, and trace system  
data/ contains a small notes file for retrieval tests  
examples/ contains sample runs

## Next improvements
- Plug in a real LLM planner (local model or API)
- Add tool permissioning and safety constraints
- Add unit tests and evaluation harness
- Add multi-step tool chaining with verification

### Command-Line Interface (CLI)

MiniAgent exposes a clean CLI interface using `argparse`, allowing tasks to be executed in a reproducible and testable way.

Example usage:

```bash
python -m miniagent.cli --task "calculate (4*3)/5"
python -m miniagent.cli --task "lookup notes: hallucinations"

_Last verified: December 17, 2025_
