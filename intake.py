"""module for parsing intake lines
provides a function parse_intake_line(line) that takes a line of text and returns a dictionary with keys "item", "category", and "minutes" if the line is valid, or raises a ValueError if the line is invalid.
"""
import subprocess
def parse_intake_line(line):
    parts = line.split("|")
    if len(parts) != 3:
        raise ValueError("expected 3 fields, got " +str(len(parts)))
    item = parts[0].strip()
    category = parts[1].strip().lower()
    minutes_text = parts[2].strip()
    if item == "" or category == "":
        raise ValueError("item and category must not be empty")
    minutes = int(minutes_text)
    if minutes <= 0:
        raise ValueError("minutes must be greater than zero")
    return {"item": item, "category": category,"minutes": minutes}
test_output = parse_intake_line("laptop | electronics | 60")
print(test_output)