import subprocess
import unittest
from intake import parse_intake_line
class ParseIntakeLineTests(unittest.TestCase):
    def test_valid_line_is_split_and_trimmed(self):
        record = parse_intake_line("desk lamp | electrical | 40")
        self.assertEqual(record, {"item": "desk lamp", "category": "electrical", "minutes": 40})
    def test_minutes_become_an_integer(self):
        record = parse_intake_line("kettle|electrical|20")
        self.assertIsInstance(record["minutes"], int)
    def test_category_is_lowercased(self):
        record = parse_intake_line("bicycle | Mechanical | 40")
        self.assertEqual(record["category"], "mechanical")
    def test_windows_line_ending_is_trimmed(self):
        record = parse_intake_line("denim jacket | textile | 20\r\n")
        self.assertEqual(record["minutes"], 20)
    def test_word_minutes_raise_value_error(self):
        with self.assertRaises(ValueError):
            parse_intake_line("radio | electrical | forty")
    def test_missing_field_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_intake_line("radio | electrical")
    def test_extra_field_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_intake_line("radio | electrical | 40 | urgent")
    def test_blank_item_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_intake_line(" | electrical | 40")
    def test_zero_or_negative_minutes_raise_value_error(self):
        with self.assertRaises(ValueError):
            parse_intake_line("radio | electrical | 0")
        with self.assertRaises(ValueError):
            parse_intake_line("radio | electrical | -5")
if __name__ == "__main__":
    unittest.main()
