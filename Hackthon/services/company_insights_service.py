from openai import OpenAI
import json

client = OpenAI(api_key="Enter you key")

def get_company_insights(company_name):
    prompt = f"""
Act as a Business Research Analyst. 
Give a structured JSON response with the following keys for the company '{company_name}':
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
            model="gpt-4o",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful business research AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        reply = response.choices[0].message.content
        return json.loads(reply)

    except Exception as e:
        print(f"Error fetching company insights: {e}")
        return {"error": str(e)}
