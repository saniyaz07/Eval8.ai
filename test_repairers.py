import unittest

from repairers import (REPAIRERS,
                        choose_repairer,
                        format_money,
                        qualified_repairers,
                        quote_cents,
                        starting_minutes,)
class QualifiedRepairersTests(unittest.TestCase):
    def test_electrical_matches_ana_and_ben(self):
        self.assertEqual(qualified_repairers("electrical", REPAIRERS), ["Ana", "Ben"])
    def test_textile_matches_ana_and_cleo(self):
        self.assertEqual(qualified_repairers("textile", REPAIRERS), ["Ana", "Cleo"])
    def test_unknown_category_matches_nobody(self):
        self.assertEqual(qualified_repairers("plumbing", REPAIRERS), [])
class ChooseRepairerTests(unittest.TestCase):
    def test_most_minutes_remaining_wins(self):
        remaining = {"Ana": 50, "Ben": 60}
        self.assertEqual(choose_repairer(["Ana", "Ben"], remaining, 20), "Ben")
    def test_repairer_without_enough_time_is_skipped(self):
        remaining = {"Ana": 90, "Ben": 60}
        self.assertEqual(choose_repairer(["Ben"], remaining, 70), None)
    def test_exactly_enough_time_is_enough(self):
        remaining = {"Ben": 40}
        self.assertEqual(choose_repairer(["Ben"], remaining, 40), "Ben")
    def test_tie_goes_to_first_listed(self):
        remaining = {"Ana": 30, "Cleo": 30}
        self.assertEqual(choose_repairer(["Ana", "Cleo"], remaining, 10), "Ana")
    def test_no_qualified_repairers_gives_none(self):
        self.assertIsNone(choose_repairer([], {"Ana": 90}, 10))
class StartingMinutesTests(unittest.TestCase):
    def test_copy_does_not_change_the_records(self):
        remaining = starting_minutes(REPAIRERS)
        remaining["Ana"] = 0
        self.assertEqual(REPAIRERS[0]["minutes"], 90)
class QuoteTests(unittest.TestCase):
    def test_forty_minutes_costs_eight(self):
        self.assertEqual(format_money(quote_cents(40)), "8.00")
        self.assertEqual(format_money(0), "0.00")

    def test_seven_minutes_costs_three_oh_five(self):
        self.assertEqual(format_money(quote_cents(7)), "3.05")

    def test_format_money_pads_cents(self):
        self.assertEqual(format_money(2605), "26.05")
        self.assertEqual(format_money(0), "0.00")
        # self.assertEqual(REPAIRERS[0]["minutes"], 90)

if __name__ == "__main__":
    unittest.main()