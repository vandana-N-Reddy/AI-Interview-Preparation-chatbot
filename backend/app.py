
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Create OpenAI client lazily so the app can start even if the key is missing.
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "PASTE_YOUR_API_KEY_HERE":
        return None
    return OpenAI(api_key=api_key)


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    client = get_openai_client()
    if client is None:
        return (
            jsonify({"error": "OPENAI_API_KEY not set. Add it to backend/.env or set the environment variable."}),
            500,
        )

    data = request.json or {}
    prompt = f"""Create a detailed daily study plan.
Subject: {data.get('subject')}
Study hours per day: {data.get('hours')}
Exam date: {data.get('exam_date')}
Skill level: {data.get('level')}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        return jsonify({"error": "OpenAI request failed", "details": str(e)}), 502

    # Fallback if response shape differs
    try:
        content = response.choices[0].message.content
    except Exception:
        content = getattr(response, "text", None) or str(response)

    return jsonify({"study_plan": content})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
