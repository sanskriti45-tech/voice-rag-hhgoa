import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

UNSAFE_PATTERNS = [
    r"\b(kill|suicide|self[\s-]?harm|bomb|weapon|attack)\b",
    r"\b(hack|exploit|malware|ddos)\b",
]

OFF_TOPIC_SCORE_THRESHOLD = 0.15

REFUSAL_MESSAGE = "I can't help with that request."
OFF_TOPIC_MESSAGE = "That question doesn't appear to be covered by this system's dataset."
NOT_GROUNDED_MESSAGE = "I don't have enough grounded information in the retrieved context to answer that confidently."


def check_unsafe_input(query: str) -> bool:
    """Returns True if the query matches an unsafe/inappropriate pattern."""
    lowered = query.lower()
    return any(re.search(pattern, lowered) for pattern in UNSAFE_PATTERNS)


def check_off_topic(retrieved_results, threshold: float = OFF_TOPIC_SCORE_THRESHOLD) -> bool:
    """Returns True if the query is likely off-topic (poor retrieval match)."""
    if not retrieved_results:
        return True
    top_score = retrieved_results[0][1] if isinstance(retrieved_results[0], tuple) else 0
    return top_score < threshold


def check_grounded(answer_text: str, context: str) -> bool:
    """Returns True if the answer's claims are supported by the retrieved context."""
    if not answer_text or not context:
        return False

    judge_prompt = f"""Does the ANSWER below rely only on facts present in the CONTEXT?
Reply with exactly one word: YES or NO.

CONTEXT:
{context}

ANSWER:
{answer_text}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": judge_prompt}],
            temperature=0,
            max_tokens=5,
        )
        verdict = response.choices[0].message.content.strip().upper()
        return verdict.startswith("YES")
    except Exception as e:
        print(f"[grounding check error] {e}")
        return False


def apply_guardrails(query: str, retrieved_results, generated_result: dict) -> dict:
    """
    Runs all four required guardrail checks in order.
    Returns {'allowed': bool, 'final_answer': str, 'reason': str}
    """
    if check_unsafe_input(query):
        return {"allowed": False, "final_answer": REFUSAL_MESSAGE, "reason": "unsafe_input"}

    if check_off_topic(retrieved_results):
        return {"allowed": False, "final_answer": OFF_TOPIC_MESSAGE, "reason": "off_topic"}

    if not generated_result.get("success"):
        return {"allowed": False, "final_answer": NOT_GROUNDED_MESSAGE, "reason": "generation_failed"}

    answer_text = generated_result.get("answer", "")
    context = generated_result.get("context_used", "")

    if not check_grounded(answer_text, context):
        return {"allowed": False, "final_answer": NOT_GROUNDED_MESSAGE, "reason": "not_grounded"}

    return {"allowed": True, "final_answer": answer_text, "reason": "passed"}