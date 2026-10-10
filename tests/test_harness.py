import copy
import unittest

from scripts.prove import REQUIRED, control_rejected, passes


class Harness(unittest.TestCase):
    def test_zero_exercise_cannot_support_a_positive_claim(self):
        result = {"claims": {name: True for name in REQUIRED}, "exercised": {name: 1 for name in REQUIRED}}
        self.assertTrue(passes(result))
        for name in REQUIRED:
            bad = copy.deepcopy(result)
            bad["exercised"][name] = 0
            self.assertFalse(passes(bad))

    def test_a_control_must_fail_for_its_targeted_reason(self):
        result = {"claims": {name: name != "restart" for name in REQUIRED},
                  "exercised": {name: 1 for name in REQUIRED},
                  "failures": {"restart": "AssertionError: acknowledged task absent in fresh process"}}
        self.assertTrue(control_rejected("volatile", result))
        result["failures"]["restart"] = "RuntimeError: child process failed to start"
        self.assertFalse(control_rejected("volatile", result))

    def test_a_control_that_did_not_run_cannot_validate_the_harness(self):
        result = {"claims": {name: False for name in REQUIRED},
                  "exercised": {name: 0 for name in REQUIRED},
                  "failures": {"restart": "AssertionError: acknowledged task absent in fresh process"}}
        self.assertFalse(control_rejected("volatile", result))


if __name__ == "__main__":
    unittest.main()
