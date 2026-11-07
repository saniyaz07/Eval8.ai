"""FixDesk: triage repair-cafe intake lines, assign repairers, print quotes."""
import subprocess
from intake import parse_intake_line
from repairers import (
    REPAIRERS,SKILL_FOR_CATEGORY,choose_repairer,format_money, qualified_repairers,quote_cents,starting_minutes,)
SAMPLE_INTAKE = [
    "desk lamp | electrical | 40",
    "kettle | electrical | 20",
    "bicycle | mechanical | 40",
    "denim jacket | textile | 20",
    "radio | electrical | forty",
    "sewing machine | mechanical | 30",
]
def run_session(lines, repairers):
    """Process every intake line and return the report"""
    output = []
    results = []
    remaining = starting_minutes(repairers)
    for line in lines:
        try:
            record = parse_intake_line(line)
        except ValueError:
            output.append("Skipped: " + line.strip() + " (invalid minutes)")
            continue
        item = record["item"]
        qualified = qualified_repairers(record["category"], repairers)
        if qualified:
            output.append(item + " -> qualified: " + ", ".join(qualified))
        else:
            output.append(item + " -> qualified: none")
        assignee = choose_repairer(qualified, remaining, record["minutes"])
        if assignee is None:
            output.append(item + ": unassigned, no qualified repairer has time")
            quote = 0
        else:
            remaining[assignee] = remaining[assignee] - record["minutes"]
            quote = quote_cents(record["minutes"])
            output.append(item + ": assigned to " + assignee + ", quote " + format_money(quote))
        results.append({"category": record["category"],
                        "assignee": assignee,
                        "quote": quote})
    output.extend(summary_lines(results))
    return output
def summary_lines(results):
    """Build the session summary from the per-item"""
    quotes = [r["quote"] for r in results if r["assignee"] is not None]
    unassigned = [r for r in results if r["assignee"] is None]
    lines = ["--- Session summary ---", "Items: " + str(len(results))]
    for category in SKILL_FOR_CATEGORY:
        count = len([r for r in results if r["category"] == category])
        lines.append(category + ": " + str(count))
    other = len([r for r in results if r["category"] not in SKILL_FOR_CATEGORY])
    if other > 0:
        lines.append("other: " + str(other))
    lines.append("Unassigned: " + str(len(unassigned)) + " | Total quoted: " + format_money(sum(quotes)))
    return lines
def main():
    print("FixDesk session")
    for text in run_session(SAMPLE_INTAKE, REPAIRERS):
        print(text)
if __name__ == "__main__":
    main()
