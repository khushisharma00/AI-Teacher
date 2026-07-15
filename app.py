from flask import Flask, render_template, request
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = Flask(__name__)

lesson = ""


@app.route("/")
def home():
    return render_template(
        "index.html",
        lesson="",
        doubt_answer=""
    )


@app.route("/teach", methods=["POST"])
def teach():
    global lesson

    topic = request.form["topic"]

    prompt = f"""
You are an AI Teacher.

Teach this topic in very easy language.

Rules:
1. Start with definition.
2. Explain step by step.
3. Give one real-life example.
4. Give important points.
5. End with:
Do you have any doubts?

Topic:
{topic}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    lesson = response.text

    return render_template(
        "index.html",
        lesson=lesson,
        doubt_answer=""
    )


@app.route("/doubt", methods=["POST"])
def doubt():
    global lesson

    doubt = request.form["doubt"]

    prompt = f"""
You are an AI Teacher.

Previously you taught:

{lesson}

Student doubt:

{doubt}

Answer in very easy language.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return render_template(
        "index.html",
        lesson=lesson,
        doubt_answer=response.text
    )


if __name__ == "__main__":
    app.run(debug=True)