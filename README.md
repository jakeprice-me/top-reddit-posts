# Top Reddit Posts

## Summary

In an effort to have media and news come to me (as opposed to digitally mining for it), I've made this really simple script to go and get the top 10 posts from a selection of sub-reddits, over the past week.

## Output

The script will output a one-page HTML page, `index.html` into the `public/` directory.

## Usage

Clone this repository to your device.

### Python Reddit API Wrapper Module

Make sure you install PRAW.

```sh
pip install praw
```

### Reddit API Application

Then you need a set of Reddit API credentials. Go [here](https://old.reddit.com/prefs/apps/) and click `create another app...`

Fill in the following fields:

![](.images/reddit_app_1.png)

Then click `create app` and you'll see something like the below. 

![](.images/reddit_app_2.png)

I've obfuscated the credentials in the screenshot, but item 1 corresponds to `client_id` and 2 to `client_secret` in the `config.py` file below.

### Configuration File

_Create_ a file called `.config.py` in the cloned repository and provide values to the below configuration variables. The script won't run without a valid `config.py`.

Add as many sub-reddits as you like, just make sure they are surrounded by double-quotes, and delimited by a comma. You may also want to sort them, as this is the order they will be output in. Equally though that gives you the option to manually sort them - perhaps with sub-reddits you're more interested in at the top and so on.

```py
client_id = "<reddit-app-id>"
client_secret = "<reddit-app-secret>"
client_user_agent = (
    "<reddit-app-description>"
)
script_directory = "<path to repository folder>"
period = "week"
posts = <number-of-posts>
subreddits = [
    "subreddit1",
    "subreddit2",
]
```

### Run

You can run the script manually, but I run it once a week using cron and mount the repository to a Docker container, serving it up on my local network using Caddy. That way I can visit the local URL I use and see the latest list of top posts.

An example entry for `crontab` can be found below.

```bash
# Run top reddit posts:
50 5 * * sat python3 <path-to-repo>/get-posts.py
```

