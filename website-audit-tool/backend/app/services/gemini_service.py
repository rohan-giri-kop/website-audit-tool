import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import re

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_recommendations(findings):

    try:

        prompt = f"""
        You are a professional Website Audit Expert.

        Audit Findings:

        {findings}

        Return ONLY valid JSON.

        Example:

        [
          {{
            "priority": "High",
            "recommendation": "Fix missing meta description"
          }}
        ]

        No markdown.
        No explanations.
        """

        response = model.generate_content(prompt)

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        recommendations = json.loads(text)

        if not isinstance(recommendations, list):
            recommendations = []

        return recommendations

    except Exception as e:

        print("Gemini Error:", str(e))

        return []