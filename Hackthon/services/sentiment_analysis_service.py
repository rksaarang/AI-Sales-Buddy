from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="enter your key")  # Replace with your actual key

def analyze_sentiment(text):
    try:
        prompt = f"""
        Analyze the following meeting note content and classify the overall client sentiment as Positive, Neutral, or Negative.
        Meeting Note:
        {text}

        Respond only with one word: Positive, Neutral, or Negative.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        sentiment = response.choices[0].message.content.strip()
        return sentiment

    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Unknown"
