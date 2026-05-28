from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List, Mapping
import json
import re


def _case_id(*parts: str) -> str:
    slug = "-".join(parts).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug or "case"


def mutate_value(value: Any) -> List[Dict[str, Any]]:
    mutations: List[Dict[str, Any]] = [{"kind": "identity", "value": deepcopy(value)}]
    if isinstance(value, str):
        mutations.extend(
            [
                {"kind": "leading_trailing_space", "value": f"  {value}  "},
                {"kind": "newline_wrapped", "value": f"\n{value}\n"},
                {"kind": "case_flip", "value": value.swapcase()},
            ]
        )
        if "," in value:
            mutations.append({"kind": "extra_delimiter_space", "value": value.replace(",", " , ")})
    elif isinstance(value, list):
        mutations.append({"kind": "reversed", "value": list(reversed(value))})
        mutations.append({"kind": "duplicated_tail", "value": list(value) + list(value[-1:])})
    elif isinstance(value, dict):
        keys = sorted(value)
        mutations.append({"kind": "sorted_keys", "value": {key: value[key] for key in keys}})
        if keys:
            changed = deepcopy(value)
            first = keys[0]
            changed[first] = mutate_value(value[first])[-1]["value"]
            mutations.append({"kind": f"nested_{first}", "value": changed})
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        mutations.extend(
            [
                {"kind": "zero", "value": 0},
                {"kind": "negative", "value": -abs(value)},
                {"kind": "large", "value": value * 1000 + 1},
            ]
        )
    return mutations


def generate_cases(spec: Mapping[str, Any]) -> List[Dict[str, Any]]:
    name = str(spec.get("name", "spec"))
    invariants = list(spec.get("invariants", ["idempotent"]))
    examples = list(spec.get("examples", []))
    cases: List[Dict[str, Any]] = []
    seen = set()
    for index, example in enumerate(examples):
        for invariant in invariants:
            for mutation in mutate_value(example):
                case_id = _case_id(name, str(index), str(invariant), mutation["kind"])
                if case_id in seen:
                    continue
                seen.add(case_id)
                cases.append(
                    {
                        "id": case_id,
                        "spec": name,
                        "invariant": invariant,
                        "original": deepcopy(example),
                        "mutated": mutation["value"],
                        "mutation": mutation["kind"],
                        "assertion": assertion_text(str(invariant)),
                    }
                )
    return cases


def assertion_text(invariant: str) -> str:
    if invariant == "idempotent":
        return "f(f(mutated)) == f(mutated)"
    if invariant == "roundtrip":
        return "decode(encode(mutated)) == mutated"
    if invariant == "whitespace_stable":
        return "f(mutated) == f(original) for whitespace-only mutations"
    if invariant == "order_insensitive":
        return "f(mutated) == f(original) for order-only mutations"
    return f"custom invariant: {invariant}"


def render_pytest(cases: Iterable[Mapping[str, Any]], target: str) -> str:
    module, _, func = target.rpartition(".")
    if not module or not func:
        raise ValueError("target must look like 'module.function'")
    lines = [
        "import pytest",
        f"from {module} import {func} as target",
        "",
        "CASES = " + json.dumps(list(cases), indent=2, sort_keys=True),
        "",
        "@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])",
        "def test_metamorphic_case(case):",
        "    if case['invariant'] == 'idempotent':",
        "        assert target(target(case['mutated'])) == target(case['mutated'])",
        "    elif case['invariant'] in {'whitespace_stable', 'order_insensitive'}:",
        "        assert target(case['mutated']) == target(case['original'])",
        "    else:",
        "        pytest.skip(f\"No executable template for {case['invariant']}\")",
        "",
    ]
    return "\n".join(lines)


def demo_spec() -> Dict[str, Any]:
    return {
        "name": "url_normalizer",
        "invariants": ["idempotent", "whitespace_stable"],
        "examples": ["HTTPS://Example.com/a/../b?q=1,2", " http://localhost:80/index.html "],
    }
