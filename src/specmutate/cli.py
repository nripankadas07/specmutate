from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from .core import demo_spec, generate_cases, render_pytest


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="specmutate")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="generate demo metamorphic cases")
    demo.add_argument("--json", action="store_true")
    demo.add_argument("--pytest", metavar="MODULE.FUNCTION")
    args = parser.parse_args(argv)
    if args.command == "demo":
        cases = generate_cases(demo_spec())
        if args.pytest:
            print(render_pytest(cases, args.pytest))
        elif args.json:
            print(json.dumps(cases, indent=2, sort_keys=True))
        else:
            print(f"generated {len(cases)} metamorphic cases")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
