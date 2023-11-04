from hashtag_scraper import *
from tweet_generator import *


hashtag = ""
tweets_scraped = scrape_tweets(hashtag, 5)
prompt = f"Write tweet impersonating Marcus Aurelius in json format that has one object called tweet based on the following tweets: {tweets_scraped}"
print(generate_tweets(prompt, 2))
