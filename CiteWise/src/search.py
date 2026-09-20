import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "academic_sources.json"

STOPWORDS = {
    "the","a","an","and","or","of","to","in","for","on","with","is","are",
    "was","were","that","this","these","those","as","by","from","has","have",
    "had","be","been","can","may","using","used","their","our","we","they",
    "it","its","into","than","also","based","such","which","more","most"
}

def tokens(text):
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}

class AcademicSearcher:
    def __init__(self):
        with open(DATASET, "r", encoding="utf-8") as f:
            self.sources = json.load(f)

    def best_match(self, claim):
        ct = tokens(claim)
        best = None
        best_score = 0.0
        best_overlap = set()

        for source in self.sources:
            corpus = " ".join([
                source["title"], source["abstract"], source["venue"]
            ])
            st = tokens(corpus)
            overlap = ct & st
            if not ct:
                score = 0
            else:
                score = len(overlap) / math.sqrt(len(ct) * max(len(st), 1))
                score = min(score * 2.8, 1.0)

            if score > best_score:
                best_score = score
                best = source
                best_overlap = overlap

        reason = (
            "Relevant terms overlap with the source title/abstract: "
            + ", ".join(sorted(best_overlap)[:10])
            if best else ""
        )
        return best, best_score, reason
