"""Turn coverage.json (pytest-cov) into a Markdown comment for the pull request."""

import json
import os
import sys


def percent(covered: int, total: int) -> str:
    return f"{100 * covered / total:.1f}%" if total else "n/a"


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        report = json.load(f)
    totals = report["totals"]
    lines = [
        "## Test coverage",
        "",
        f"Commit: `{os.environ.get('HEAD_SHA', 'local')[:7]}`",
        "",
        "| Type | Covered | Total | Coverage |",
        "|---|---|---|---|",
        f"| Lines | {totals['covered_lines']} | {totals['num_statements']} "
        f"| **{percent(totals['covered_lines'], totals['num_statements'])}** |",
        f"| Branches | {totals['covered_branches']} | {totals['num_branches']} "
        f"| **{percent(totals['covered_branches'], totals['num_branches'])}** |",
        "",
        "| File | Lines | Branches | Missing lines |",
        "|---|---|---|---|",
    ]
    for name, data in sorted(report["files"].items()):
        s = data["summary"]
        missing = ", ".join(str(n) for n in data["missing_lines"]) or "-"
        lines.append(
            f"| `{name}` | {percent(s['covered_lines'], s['num_statements'])} "
            f"| {percent(s['covered_branches'], s['num_branches'])} | {missing} |"
        )
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
