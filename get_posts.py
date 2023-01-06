# *****************************************************************************
# Top Reddit Posts
# *****************************************************************************

# ==== Modules ================================================================

import json
from datetime import datetime
import praw
import requests
import config

# ==== Functions ==============================================================


def get_posts():

    # Set period to retrieve post over:
    period = config.period

    # Set number of posts to retrieve from each sub-reddit:
    posts = config.posts

    run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Initiate praw:
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.client_user_agent,
    )

    # Get list of sub-reddits:
    subreddit_list = config.subreddits

    # Get path to public directory:
    script_directory = config.script_directory

    with open(f"{script_directory}/public/index.html", "w", encoding="utf-8") as index:

        html_header = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <title>The Week's Top Sub-Reddit Posts</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link rel="stylesheet" href="assets/css/stylesheet.css">
</head>
<body>
<main>
<h1>The Week's Top Sub-Reddit Posts</h1>
<p>Last Updated: {run_date}</p>"""

        index.write(html_header)

        for subreddit in subreddit_list:
            print(subreddit)
            output = f"""
<h2>r/{subreddit}</h2>
<ul>"""
            index.write(output)

            for submission in reddit.subreddit(subreddit).top(
                time_filter=period, limit=posts
            ):

                permalink = submission.permalink
                title = submission.title

                item_output = f"""
<li><a href="https://reddit.com{permalink}" target="_blank">{title}</a> <a href="https://old.reddit.com{permalink}" target="_blank">[o]</a> <a href="https://i.reddit.com{permalink}" target="_blank">[i]</a></li>"""

                index.write(item_output)

            index.write("</ul>")

        footer = """
</main>
</body>
</html>"""
        index.write(footer)

    # Gotify API Configuration:
    token = config.gotify_app_token
    base_url = config.gotify_base_url
    api_url = f"/message?token={token}"
    api_payload = {
        "priority": 4,
        "title": "Top Reddit Posts",
        "message": "Latest issue available [here](https://trp.int.ppn.sh)...",
        "extras": {
            "client::display": {"contentType": "text/markdown"},
        },
    }
    api_endpoint = base_url + api_url

    # Gotify API call:
    requests.post(
        api_endpoint,
        headers={"Content-Type": "application/json"},
        data=json.dumps(api_payload),
    )


get_posts()
