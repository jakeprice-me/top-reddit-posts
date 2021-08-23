# *****************************************************************************
# Top Reddit Posts
# *****************************************************************************

# ==== Modules ================================================================

import config
import praw
from datetime import datetime

# ==== Functions ==============================================================


def getPosts():

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

    with open(f"{script_directory}/public/index.html", "w") as index:

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
            output = f"""
<h2>r/{subreddit}</h2>
<ul>"""
            index.write(output)

            for submission in reddit.subreddit(subreddit).top(
                time_filter=config.period, limit=config.posts
            ):

                permalink = submission.permalink
                title = submission.title

                item_output = f"""
<li><a href="https://reddit.com{permalink}" target="_blank">{title}</a></li>"""

                index.write(item_output)

            index.write("</ul>")

        footer = """
</main>
</body>
</html>"""
        index.write(footer)


getPosts()
