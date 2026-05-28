import unittest

from specmutate import demo_spec, generate_cases, render_pytest


class SpecMutateTests(unittest.TestCase):
    def test_generates_unique_cases(self):
        cases = generate_cases(demo_spec())
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(cases), 8)

    def test_renders_pytest_template(self):
        text = render_pytest(generate_cases(demo_spec())[:2], "normalizer.normalize")
        self.assertIn("def test_metamorphic_case", text)
        self.assertIn("from normalizer import normalize", text)


if __name__ == "__main__":
    unittest.main()
