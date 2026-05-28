# Contributing

SpecMutate turns small behavior specs into deterministic metamorphic test
vectors. Contributions should improve generated cases, invariants, or test
renderers without hiding behavior behind a model judge.

Before opening a pull request:

- run `python -m unittest discover -s tests -v`;
- add a spec fixture for new invariant families;
- keep generated assertions readable;
- document limitations when an invariant is only a template.

