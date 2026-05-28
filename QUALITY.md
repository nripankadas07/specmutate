# Quality Notes

SpecMutate should generate deterministic, human-readable test vectors.

Current gates:

- unit tests for unique case generation and pytest rendering;
- CLI demo for JSON and pytest output;
- Python 3.9 and 3.13 CI;
- no runtime dependency on an LLM or external property-testing framework.

New invariants should include examples where the mutation is useful and cases
where the invariant would be unsafe to assume.

