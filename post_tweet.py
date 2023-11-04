import random
import pickle
import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json

# Load tweets from JSON file
with open("tweets.json") as f:
    tweets = json.load(f)


def setup_twitter():
    # # Set the path to the GeckoDriver binary in the PATH environment variable
    # geckodriver_path = "/home/xxx/geckodriver"  # Replace with the correct path
    # os.environ["PATH"] = f"{os.environ['PATH']}:{os.path.dirname(geckodriver_path)}"

    # # Set the path to the Firefox binary using an environment variable
    # os.environ[
    #     "MOZ_HEADLESS"
    # ] = "1"  # Set this to "0" if you want to run Firefox with a visible window

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

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
        username_field.send_keys(
            "username"
        )  # replace with your actual twitter username
        username_field.send_keys(Keys.RETURN)

        password_field = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(
            "password"
        )  # replace with your actual twitter password
        password_field.send_keys(Keys.RETURN)
        print("logged in")

        time.sleep(5)

        try:
            cookies = driver.get_cookies()
            pickle.dump(cookies, open("cookies.pkl", "wb"))
            print("Cookies saved to file")
        except Exception as e:
            print("Couldn't write cookies to file", e)

    return driver, wait


def post_tweet(driver, wait, tweet):
    try:
        driver.get("https://twitter.com/compose/tweet")
        # Wait until the tweet field is present
        tweet_field = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "public-DraftEditor-content")
            )
        )
        tweet_field.send_keys(tweet)
        tweet_field.send_keys(Keys.CONTROL, Keys.ENTER)
        print("tweet posted")
        return True

    except NoSuchElementException as ex:
        print("An element was not found. ", ex)
        return False
    except TimeoutException as ex:
        print("The request timed out. ", ex)
        return False


# Setup Twitter
driver, wait = setup_twitter()

# Check if setup was successful
if driver and wait:
    # Iterate over tweets and post each
    for tweet in tweets:
        if post_tweet(driver, wait, tweet["tweet"]):  # if tweet was successfully posted
            tweets.remove(tweet)  # remove tweet from list
            # update json file
            with open("tweets.json", "w") as f:
                json.dump(tweets, f)
            print("tweet deleted from json")

        time.sleep(random.randint(180, 420))  # delay between tweets

    # Close the browser
    driver.close()
