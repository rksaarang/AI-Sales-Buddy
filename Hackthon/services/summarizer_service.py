import openai

openai.api_key = 'YOUR_API_KEY'

def generate_summary(user_input):
    prompt = f"Summarize the following sales meeting notes into a short summary with action points:\n\n{user_input}\n\nSummary:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
