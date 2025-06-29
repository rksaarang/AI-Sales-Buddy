from openai import OpenAI
from datetime import datetime
import json

# Initialize OpenAI client
client = OpenAI(
    api_key="enter you key"
)

def get_company_insights(company_name):
    """
    Get detailed company insights using OpenAI API
    """
    prompt = f"""
Act as a Business Research Analyst. 
Provide a structured JSON response with the following keys for the company '{company_name}':

- title: (string, title for the insights)
- latest_developments: (array of strings, latest business news about the company)
- market_position: (string, short paragraph about their current market position)
- competitors: (array of strings, list of major competitors)
- trends: (array of strings, key market or industry trends affecting them)
- opportunities: (array of strings, business opportunities)
- challenges: (array of strings, business risks or challenges)

Respond ONLY in valid JSON format. No extra text.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5-turbo as it's more reliable
            messages=[
                {"role": "system", "content": "You are a helpful business research AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        reply = response.choices[0].message.content
        return json.loads(reply)

    except Exception as e:
        error_msg = str(e)
        if "Invalid API key" in error_msg:
            return {"error": "Invalid OpenAI API key. Please check your API key configuration."}
        elif "Rate limit" in error_msg:
            return {"error": "Rate limit exceeded. Please wait a few minutes and try again."}
        else:
            return {"error": f"Failed to fetch company insights: {error_msg}"}


def get_market_insights(sector):
    """
    Get market insights for a specific sector using OpenAI API (GPT-4o or GPT-3.5)
    """
    prompt = f"""
You are a Senior Market Research Analyst. Provide a structured JSON market analysis for the '{sector}' sector with the following fields:

- title: (string, title for the insights)
- summary: (string, summary of sector condition)
- trends: (array of strings, current market trends)
- opportunities: (array of strings, business opportunities)
- risks: (array of strings, sector-specific challenges/risks)
- recent_events: (array of strings, any important events/news in the last 30 days)

Only respond with JSON. No extra explanation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a professional market research assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )

        reply = response.choices[0].message.content
        return json.loads(reply)

    except Exception as e:
        print(f"Error fetching market insights: {e}")
        return {"error": str(e)}
