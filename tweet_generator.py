import openai

# openai.api_key = 'sk-xxx'


def generate_tweets(prompt, num_tweets):
    tokens = estimate_tokens(prompt)
    print(f"the prompt is {tokens} tokens")
    print("generating tweets")
    tweets = []
    for _ in range(num_tweets):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=280
        )
        tweets.append(response.choices[0].text.strip())
    for tweet in tweets:
        tokens += estimate_tokens(tweet)
    print(f"output used {tokens} tokens")

    return tweets


def estimate_tokens(text):
    words = text.split()
    estimated_tokens = len(words) * 2  # assuming 2 tokens per word on average
    return estimated_tokens
