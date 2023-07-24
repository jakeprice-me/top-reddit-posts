# *****************************************************************************
# Top Reddit Posts
# *****************************************************************************

# ==== Modules ================================================================

from datetime import datetime
import praw
import prawcore
import config
import requests

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

    public_url = config.public_url
    trp_url = config.trp_url

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
<p>Last Updated: {run_date}</p>
<ul id="toc">
"""

        index.write(html_header)

        for subreddit in subreddit_list:
            index.write(f'<li><a href="#{subreddit}">{subreddit}</a></li>')

        index.write("</ul>")

        for subreddit in subreddit_list:
            print(subreddit)

            # Add exception handling for 403 error:
            try:
                subreddit_obj = reddit.subreddit(subreddit)
                output = f"""
<h2 id="{subreddit}">r/{subreddit}</h2>
<ul>"""
                index.write(output)

                for submission in subreddit_obj.top(time_filter=period, limit=posts):
                    permalink = submission.permalink
                    title = submission.title

                    item_output = f"""
<li><a href="https://{public_url}{permalink}" target="_blank">{title}</a> <a href="https://old.reddit.com{permalink}" target="_blank">[o]</a></li>"""

                    index.write(item_output)

                index.write("</ul>")

            except praw.exceptions.RedditAPIException as e:
                if e.error_type == "403":
                    print(
                        f"Skipped subreddit '{subreddit}' due to a 403 Forbidden error."
                    )
                else:
                    print(f"Skipped subreddit '{subreddit}' due to an error: {e}")

            except prawcore.exceptions.Forbidden:
                print(f"Skipped subreddit '{subreddit}' due to a 403 Forbidden error.")
        footer = """
</main>
</body>
</html>"""
        index.write(footer)


    # Telegram API Configuration:
    bot_token = config.telegram_bot_token
    base_url = config.telegram_base_url
    chat_id = str(config.telegram_bot_chat_id)
    api_url = f"/bot{bot_token}/sendMessage"

    # Setup the notification message:
    api_payload = {
        "chat_id": chat_id,
        "parse_mode": "HTML",
        "text": f'Latest issue available <a href="{trp_url}">here</a>...',
    }
    api_endpoint = base_url + api_url

    # Telegram API call:
    response = requests.post(
        api_endpoint,
        headers={"Content-Type": "application/json"},
        json=api_payload,
    )


get_posts()
