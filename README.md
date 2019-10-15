# GFYSearchBot
A search bot for reddit that utilises GFYCAT's search API to find GIFs based on a search and replies with MP4 and GIF links

## Usage
In any subreddit, just enter "?gfy [upto six words in square brackets]" as a comment and the bot will reply with MP4 and GIF links of the first result of GFYCAT's search.

If you do not notice a reply, it may be due to the bot being banned by the subreddit.

## Change subreddit(s)
Line 25 of gfybot.py includes r/all: subreddit = reddit.subreddit('all')  
Replace 'all' with 'yoursubreddit' for use in a single subreddit or 'subredditone+subreddittwo' if using in multiple subreddits.

## How it works
The GFYSearchBot uses PRAW (Python Reddit API Wrapper). The bot reads every comment when it is submitted to Reddit, it then checks if it has already replied (so it doesn't keep replying to the same comment). Then it checks if the comment contains "?gfy" and if there are 6 words in the square brackets. If it meets the requirements, it will make an API call to GFYCAT. If it responds 200 OK, the bot will reply to the comment with the MP4 and GIF links. The comment id will be appended to a text file to ensure it won't reply to the same comment again. (For example, if the bot is restarted)
