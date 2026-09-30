"""Module 3: linguistic tone (starter version).

IMPORTANT: this word list is a tiny placeholder so the project runs out of the box.
Your next step is to replace it with the Loughran-McDonald financial dictionary
(free download from the University of Notre Dame's Software Repository for Accounting
and Finance). Load it from a CSV instead of hard-coding lists.
"""
from .hedges import words

POSITIVE = {"strong", "record", "excellent", "robust", "pleased", "excited", "confident",
            "improved", "healthy", "opportunities", "momentum", "resilient", "positive",
            "growth", "delivered", "meaningfully", "achieved"}
NEGATIVE = {"weak", "declined", "decline", "impairment", "loss", "losses", "deteriorated",
            "challenging", "difficult", "decreased", "adverse", "risk", "uncertain",
            "litigation", "restructuring", "charge"}

SCALE = 10  # scaling so typical sentences land between -1 and +1 (tune this later)


def tone_score(text: str) -> float:
    """Linguistic tone in [-1, 1] = (positive words - negative words) / total words, scaled."""
    ws = [w.lower() for w in words(text)]
    if not ws:
        return 0.0
    pos = sum(w in POSITIVE for w in ws)
    neg = sum(w in NEGATIVE for w in ws)
    return max(-1.0, min(1.0, SCALE * (pos - neg) / len(ws)))
