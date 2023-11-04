import random
import pickle
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import json
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def scrape_tweets(hashtag, num_tweets):
    url = "https://twitter.com/hashtag/" + hashtag + "?src=hashtag_click"

    # setup driver
    options = Options()
    # options.add_argument("--headless")  # Using headless mode
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)  # wait for maximum of 10 seconds
    driver.get("https://twitter.com/login")

    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("Cookies loaded")
    except (OSError, IOError) as e:
        print("No cookie file found, logging in")

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys("username")  # replace with your actual twitter username
        username_field.send_keys(Keys.RETURN)

        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys("password")  # replace with your actual twitter password
        password_field.send_keys(Keys.RETURN)
        print("logged in")

        time.sleep(5)

        try:
            cookies = driver.get_cookies()
            pickle.dump(cookies, open("cookies.pkl", "wb"))
            print("Cookies saved to file")
        except Exception as e:
            print("Couldn't write cookies to file", e)

    driver.get(url)

    tweets = []

    print("scraping")

    while len(tweets) < num_tweets:
        # scroll to bottom to load new tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # give it some time to load new tweets
        time.sleep(2)

        # Change this part
        tweet_elements = driver.find_elements(By.CSS_SELECTOR,
                                              '.css-901oao.r-1nao33i.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0')

        for tweet_element in tweet_elements:
            tweet_text = tweet_element.text

            if tweet_text not in tweets:
                tweets.append(tweet_text)

            if len(tweets) >= num_tweets:
                break

    driver.quit()

    print(f"scraped tweets on {hashtag}")

    tweets_scraped = ' ; '.join(tweets)

    return tweets_scraped


eprint(scrape_tweets("barbenheimer", 20))
