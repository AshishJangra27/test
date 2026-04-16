from fastapi import FastAPI

from chatbot.app import app as chatbot_app
from chatbot.chatbot import funny_answer, sarcastic_answer, serious_answer
from game.app import app as game_app
from game.game import draw_card, flip_coin, roll_dice

app = FastAPI(title="Unified API", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "services": ["game", "chatbot"]}


app.mount("/game", game_app)
app.mount("/chatbot", chatbot_app)


def run_streamlit_ui() -> None:
    import streamlit as st

    st.set_page_config(page_title="Unified Game + Chatbot", layout="centered")
    st.title("Unified Game + Chatbot")
    st.write("A lightweight UI for the local game utilities and chatbot styles.")

    tabs = st.tabs(["Game", "Chatbot"])

    with tabs[0]:
        st.header("Game utilities")
        game_action = st.selectbox(
            "Choose an action",
            ["Heads or Tails", "Roll a Dice", "Draw a Card"],
        )
        if st.button("Run action"):
            if game_action == "Heads or Tails":
                result = flip_coin()
                st.success(f"Result: {result}")
            elif game_action == "Roll a Dice":
                result = roll_dice()
                st.success(f"Dice roll: {result}")
            else:
                result = draw_card()
                st.success(f"Card drawn: {result}")

    with tabs[1]:
        st.header("Chatbot styles")
        prompt = st.text_area("Enter your message", height=120)
        style = st.radio("Choose a response style", ["Funny", "Serious", "Sarcastic"])
        if st.button("Send message"):
            if not prompt.strip():
                st.error("Please enter a message first.")
            else:
                try:
                    if style == "Funny":
                        reply = funny_answer(prompt)
                    elif style == "Serious":
                        reply = serious_answer(prompt)
                    else:
                        reply = sarcastic_answer(prompt)
                    st.success("Reply received")
                    st.write(reply)
                except Exception as exc:
                    st.error(f"Could not get a response: {exc}")


if __name__ == "__main__":
    run_streamlit_ui()
