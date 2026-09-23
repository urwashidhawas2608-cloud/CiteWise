import os
import json
from groq import Groq
from groq import APIError, APIConnectionError, APITimeoutError, RateLimitError

client = None
MODEL = "llama-3.3-70b-versatile"  # fast + capable; use "llama-3.1-8b-instant" for lower latency/cost


def _get_client():
    global client
    if client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        client = Groq(api_key=api_key)
    return client


def llm_available() -> bool:
    return _get_client() is not None


def classify_claim(sentence: str):
    """LLM replacement/augmentation for needs_citation().
    Returns True/False, or None if no API key is configured or the call fails."""
    c = _get_client()
    if c is None:
        return None
    try:
        resp = c.chat.completions.create(
            model=MODEL,
            max_tokens=10,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You classify a single sentence from an academic paper. "
                        "Reply with exactly one word: YES if the sentence states a "
                        "fact, statistic, or claim that should be backed by a "
                        "citation; NO if it is a self-contained statement, opinion, "
                        "or transition sentence that needs no citation."
                    ),
                },
                {"role": "user", "content": sentence},
            ],
        )
        answer = resp.choices[0].message.content.strip().upper()
        return answer.startswith("Y")
    except (APIError, APIConnectionError, APITimeoutError, RateLimitError, IndexError, AttributeError) as e:
        print(f"[llm_agent] classify_claim failed: {e}")
        return None


def judge_relevance(claim: str, source: dict):
    """LLM re-ranking/explanation layer on top of the existing keyword search.
    Returns a dict {relevant, confidence, reason}, or None on failure/no key."""
    c = _get_client()
    if c is None:
        return None
    prompt = (
        f"Claim: {claim}\n\n"
        f"Candidate source:\nTitle: {source['title']}\n"
        f"Abstract: {source['abstract']}\n\n"
        "Does this source plausibly support the claim? "
        'Respond ONLY with JSON, no other text: '
        '{"relevant": true/false, "confidence": 0-1, "reason": "..."}'
    )
    try:
        resp = c.chat.completions.create(
            model=MODEL,
            max_tokens=200,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return json.loads(resp.choices[0].message.content)
    except (
        APIError, APIConnectionError, APITimeoutError, RateLimitError,
        json.JSONDecodeError, IndexError, KeyError, AttributeError,
    ) as e:
        print(f"[llm_agent] judge_relevance failed: {e}")
        return None