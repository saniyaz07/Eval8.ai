"""Repairer records, skill matching and quotearithmetic for FixDesk."""

import subprocess
SKILL_FOR_CATEGORY = {
    "electrical": "electrical",
    "mechanical": "mechanical",
    "textile": "textile",}
REPAIRERS = [
    {"name": "Ana", "skills": {"electrical", "textile"}, "minutes": 90},
    {"name": "Ben", "skills": {"electrical", "mechanical"}, "minutes": 60},
    {"name": "Cleo", "skills": {"textile"}, "minutes": 45},
    ]
BASE_FEE_CENTS = 200
CENTS_PER_MINUTE = 15
def qualified_repairers(category, repairers):
    """Return the names of repairers who have the skill this category needs."""
    if category not in SKILL_FOR_CATEGORY:
        return []
    skill = SKILL_FOR_CATEGORY[category]
    names = []
    for repairer in repairers:
        if skill in repairer["skills"]:
            names.append(repairer["name"])
    return names
def starting_minutes(repairers):
    """Copy each repairer's available minutes into a  fresh name -> minutes dict."""
    remaining = {}
    for repairer in repairers:
            remaining[repairer["name"]] = repairer["minutes"]
    return remaining
def choose_repairer(qualified, remaining, minutes):
    """Pick the qualified repairer with the most  minutes left who can fit the job.
    Returns None when nobody qualified has enough time. On a tie therepairer listed first wins."""
    best = None
    for name in qualified:
        if remaining[name] >= minutes:
            if best is None or remaining[name] > remaining[best]:
                    best = name
    return best
def quote_cents(minutes):
    """Base fee of 2.00 plus 0.15 per minute, kept in whole cents."""
    return BASE_FEE_CENTS + CENTS_PER_MINUTE * minutes
def format_money(cents):
    """Turn 800 into "8.00" and 2605 into "26.05"."""
    pennies = str(cents % 100)
    if len(pennies) == 1:
        pennies = "0" + pennies
    return str(cents // 100) + "." + pennies

