# miniagent/cli.py

import argparse
from .agent import MiniAgent


def main() -> None:
    """
    Command-line entrypoint for running MiniAgent.

    This parses the task provided by the user, initializes the agent,
    executes the task, and prints the final result.
    """
    parser = argparse.ArgumentParser(
        description="MiniAgent: a lightweight tool-using agentic system"
    )

    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task for the agent to execute (e.g. 'calculate (4*3)/5')"
    )

    args = parser.parse_args()

    agent = MiniAgent()
    result = agent.run(args.task)

    print("\n=== Final Answer ===")
    print(result)


if __name__ == "__main__":
    main()
