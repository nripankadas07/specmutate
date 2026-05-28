# SpecMutate

SpecMutate turns small behavior specs into metamorphic test
vectors. It targets the kinds of developer tools that coding
agents often edit: parsers, normalizers, CLIs, serializers,
and tiny infrastructure libraries.

Instead of asking an LLM whether an answer "looks right,"
SpecMutate creates deterministic families of inputs that should
preserve a declared invariant.

## Install

```bash
git clone https://github.com/nripankadas07/specmutate
cd specmutate
python -m pip install -e .
```

## Quick Start

```bash
specmutate demo --json
specmutate demo --pytest normalizer.normalize
```

## Invariants

- idempotent: `f(f(x)) == f(x)`
- roundtrip: `decode(encode(x)) == x`
- whitespace_stable: insignificant whitespace should not
  change semantic output
- order_insensitive: mapping key order should not change
  semantic output

## Development

```bash
python -m unittest discover -s tests -v
```
