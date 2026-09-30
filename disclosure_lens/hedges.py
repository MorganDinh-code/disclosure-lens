"""Module 2: hedge detection (published, tiered lexicon)."""
import re

LOW = ["may", "might", "could", "potentially", "possibly", "uncertain", "cannot guarantee",
       "subject to", "depending on"]
MODERATE = ["expects", "expect", "anticipates", "anticipate", "believes", "likely",
            "approximately", "generally", "typically"]
HIGH = ["will", "delivered", "achieved", "has", "is"]


def _find(terms: list[str], text: str) -> int:
    count = 0
    for t in terms:
        for m in re.finditer(r"\b" + re.escape(t) + r"\b", text):
            # "may" followed by a number is probably the month, not a hedge
            if t == "may" and re.match(r"\s*\d", text[m.end():]):
                continue
            count += 1
    return count


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", text)


def hedge_counts(text: str) -> dict:
    t = text.lower()
    return {"low": _find(LOW, t), "moderate": _find(MODERATE, t), "high": _find(HIGH, t)}


def hedge_density(text: str) -> float:
    """Hedge density = (low + moderate terms) / total words.

    High-certainty words are NOT hedges; they are only used for modal intensity.
    """
    n = len(words(text))
    if n == 0:
        return 0.0
    c = hedge_counts(text)
    return (c["low"] + c["moderate"]) / n


def modal_intensity(text: str):
    """Average certainty: 1 = very uncertain, 3 = very certain. None if no modal words."""
    c = hedge_counts(text)
    total = c["low"] + c["moderate"] + c["high"]
    if total == 0:
        return None
    score = c["low"] * 1 + c["moderate"] * 2 + c["high"] * 3
    return score / total
