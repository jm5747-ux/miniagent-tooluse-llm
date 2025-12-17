# miniagent/cli.py

from __future__ import annotations
import argparse
from .agent import MiniAgent

def main():
    parser = argparse.ArgumentParser(description="MiniAgent: a tool-using agentic LLM skeleton.")
    parser.add_argument("--task", type=str, required=True, help="Task to run")
    args = parser.parse_args()

    agent = MiniAgent()
    out = agent.run(args.task)

    print("\n=== PLAN ===")
    print(out["plan"])
    print("\n=== TRACE ===")
    print(out["trace"])
    print("\n=== FINAL ===")
    print(out["final"])

if __name__ == "__main__":
    main()