
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.json
    prompt = f"""Create a detailed daily study plan.
Subject: {data.get('subject')}
Study hours per day: {data.get('hours')}
Exam date: {data.get('exam_date')}
Skill level: {data.get('level')}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"study_plan": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)
