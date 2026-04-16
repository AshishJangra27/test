import os

import requests
from dotenv import load_dotenv


load_dotenv()

MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")


def _ask(message: str, style: str) -> str:
    message = (message or "").strip()
    if not message:
        raise ValueError("message must not be empty")
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set")
    prompt = f"{style}\nKeep reply short (1-3 lines).\nUser: {message}"
    response = requests.post(
        f"{API_URL}?key={API_KEY}",
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Gemini request failed: {response.status_code}")

    data = response.json()
    text = ((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or [{}]
    answer = text[0].get("text", "").strip()
    if not answer:
        raise RuntimeError("Empty response from Gemini")
    return answer


def funny_answer(user_input: str) -> str:
    return _ask(user_input, "Reply in a funny and playful tone.")


def serious_answer(user_input: str) -> str:
    return _ask(user_input, "Reply in a serious and professional tone.")


def sarcastic_answer(user_input: str) -> str:
    return _ask(user_input, "Reply with light sarcasm, stay safe and non-abusive.")


# print(funny_answer("Why did the chicken cross the road?"))
# print(serious_answer("Why did the chicken cross the road?"))
# print(sarcastic_answer("Why did the chicken cross the road?"))