import json
from datetime import datetime

import praw
import requests


with open("./config.json") as f:
    data = json.load(f)
    client_id = data["reddit_client_id"]
    client_secret = data["reddit_client_secret"]
    flair = data["flair"]

reddit = praw.Reddit(client_id=f"{client_id}", client_secret=f"{client_secret}", user_agent="Valo")


def hls_scrape(flair=flair):
    """
    It takes the subreddit name, searches for posts with the flair "US-E", and returns the title, url, created time, author,
    and flair of the post
    :return: A dictionary with a status code and a list of dictionaries.
    """
    sub = ['homelabsales']  # make a list of subreddits you want to scrape the data from
    api = []
    for s in sub:
        subreddit = reddit.subreddit(s)

        for submission in subreddit.search(f'flair:"{flair}"', sort="new", limit=20):
            title = submission.title
            post_id = submission.id
            url = submission.url
            created = submission.created
            # body = submission.selftext
            flair = submission.link_flair_text
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "3600",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
            }

            URL = f"https://api.reddit.com/api/info/?id=t3_{post_id}"
            response = requests.get(URL, headers=headers)
            status = response.status_code
            if "[FS]" in title:
                api.append(
                    {
                        "title": title,
                        "url_path": url,
                        "created": convert_time(created),
                        "author": response.json()["data"]["children"][0]["data"]["author"],
                        "flair": flair,
                    }
                )

        data = {"status": status, "data": api}
        if status != 200:
            raise Exception("API response: {}".format(status))
        return data


def convert_time(time):
    """
    This function takes in a time in seconds and converts it to a string in the format of "mm/dd/yyyy hh:mm AM/PM"

    :param time: the time of the post
    :return: the time in a 12 hour format.
    """
    time = datetime.fromtimestamp(time)
    # convert time to 12 hour format eastern time
    time = time.strftime("%m/%d/%Y %I:%M %p")
    return time


if __name__ == '__main__':
    print(hls_scrape())