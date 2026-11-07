import subprocess
import unittest
from fixdesk import SAMPLE_INTAKE, run_session
from repairers import REPAIRERS

class SampleSessionTests(unittest.TestCase):
    def setUp(self):
        self.output = run_session(SAMPLE_INTAKE, REPAIRERS)
    def test_qualified_line(self):
        self.assertIn("desk lamp -> qualified: Ana, Ben", self.output)
    def test_assignment_and_quote_line(self):
        self.assertIn("desk lamp: assigned to Ana, quote 8.00", self.output)
        self.assertIn("kettle: assigned to Ben, quote 5.00", self.output)
    def test_invalid_line_is_skipped(self):
        self.assertIn("Skipped: radio | electrical | forty (invalid minutes)", self.output)
    def test_item_without_time_is_unassigned(self):
        self.assertIn("sewing machine: unassigned, no qualified repairer has time", self.output)
    def test_summary_ends_with_totals(self):
        self.assertEqual(self.output[-1], "Unassigned: 1 | Total quoted: 26.00")
    def test_category_tally(self):
        self.assertIn("electrical: 2", self.output)
        self.assertIn("mechanical: 2", self.output)
        self.assertIn("textile: 1", self.output)
    def test_running_twice_gives_the_same_report(self):
        self.assertEqual(run_session(SAMPLE_INTAKE, REPAIRERS), self.output)
class OtherSessionTests(unittest.TestCase):
    def test_unknown_category_is_unassigned_and_tallied_as_other(self):
        output = run_session(["garden hose | plumbing | 15"], REPAIRERS)
        self.assertEqual(output[0], "garden hose -> qualified: none")
        self.assertIn("other: 1", output)
        self.assertEqual(output[-1], "Unassigned: 1 | Total quoted: 0.00")
            
    def test_empty_intake(self):
        output = run_session([], REPAIRERS)
        self.assertEqual(output[-1], "Unassigned: 0 | Total quoted: 0.00")
if __name__ == "__main__":
    unittest.main()

        