import io
import os
import re
from typing import List, Dict

from dotenv import load_dotenv
from pypdf import PdfReader

from src.search import AcademicSearcher
from src.citations import format_source

load_dotenv()

def extract_text(data: bytes, filename: str) -> str:
    if filename.lower().endswith(".txt"):
        return data.decode("utf-8", errors="ignore")
    reader = PdfReader(io.BytesIO(data))
    return "\n".join((page.extract_text() or "") for page in reader.pages)

def split_claims(text: str) -> List[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    return [s.strip() for s in sentences if 35 <= len(s.strip()) <= 500]

def needs_citation(sentence: str) -> bool:
    s = sentence.lower()
    signals = [
        "previous studies", "research shows", "according to", "et al.",
        "has been shown", "in recent studies", "survey", "dataset",
        "accuracy", "achieved", "significantly", "outperformed",
        "proposed", "found that", "reported", "percentage", "percent",
        "increase", "decrease", "machine learning", "deep learning",
        "neural network", "artificial intelligence"
    ]
    return any(x in s for x in signals)

def analyze_document(data: bytes, filename: str, style: str) -> Dict:
    text = extract_text(data, filename)
    sentences = split_claims(text)
    claims = []
    for i, sentence in enumerate(sentences[:80], 1):
        claims.append({
            "claim_id": f"C{i:02d}",
            "text": sentence,
            "needs_citation": needs_citation(sentence),
        })

    candidates = [c for c in claims if c["needs_citation"]]
    searcher = AcademicSearcher()
    matches = []
    activity = [
        "✓ Document uploaded",
        f"✓ Extracted approximately {len(text.split())} words",
        f"✓ Identified {len(claims)} candidate statements",
        f"✓ Detected {len(candidates)} statements that may require citations",
        "🔍 Searching the included academic-source dataset...",
    ]

    for claim in candidates:
        source, score, reason = searcher.best_match(claim["text"])
        if source and score >= 0.45:
            matches.append({
                "claim_id": claim["claim_id"],
                "claim": claim["text"],
                "title": source["title"],
                "authors": source["authors"],
                "year": source["year"],
                "venue": source["venue"],
                "doi": source.get("doi", ""),
                "abstract": source["abstract"],
                "score": score,
                "reason": reason,
            })

    activity += [
        f"✓ Retrieved {len(searcher.sources)} candidate academic records",
        f"✓ Matched {len(matches)} claims with relevant sources",
        "🧠 Applied semantic/keyword relevance checks",
        "✓ Generated citation-ready metadata",
        "✓ Human review is recommended before submission",
    ]

    coverage = (len(matches) / len(candidates) * 100) if candidates else 100.0

    return {
        "claims": claims,
        "citation_candidates": candidates,
        "matches": matches,
        "coverage": coverage,
        "activity": activity,
        "style": style,
    }
