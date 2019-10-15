import praw
import pdb
import requests
import json
import re
import os


# Create the Reddit instance and log in
reddit = praw.Reddit(user_agent='your-user-agent-name',
                  client_id='your-client-id',
                  client_secret='your-client-secret',
                  username='username', password='password')

# Create a list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

# Stream of comments
subreddit = reddit.subreddit('all')
comments = subreddit.stream.comments()

for comment in comments:
    text = comment.body.lower()
    numberOfWords = len(text.split())

    # Make sure you didn't already reply to this post
    if comment.author != "GFYSearchBot":
        if comment.id not in posts_replied_to:
            # Not case sensitive
            if "?gfy" in text:
                bracketedText = re.search('\[(.*?)\]', text)
                withinBracketsText = bracketedText.group(1)
                # Less than 6 words
                wordsInBrackets = len(withinBracketsText.split())
                if wordsInBrackets > 6:
                    comment.reply("There are more than 6 words in brackets so search will not be completed")
                elif wordsInBrackets == 0:
                    comment.reply("There must be at least one word for search to complete")
                else:
                    # Reply
                    searchText = withinBracketsText.replace(" ", "+")
                    response = requests.get("https://api.gfycat.com/v1/gfycats/search?search_text={0}&count=1".format(searchText))
                    if response.status_code == 200:
                        data = response.json()
                        extractedMP4 = data["gfycats"][0]["mp4Url"]
                        extractedGIF = data["gfycats"][0]["gifUrl"]
                        message = \
                        """
**GFY Results for {0}:**

[MP4 Link - Gfycat]({1})
                        
[GIF Link - Gfycat]({2})
                        
*****
^Beep boop. ^I am ^a bot, ^and this ^action was ^performed automatically.
*****
This bot finds the first result for your gfycat search, and replies to your comment.  
*****
**Usage:** `?gfy [upto six words in square brackets]`
*****
                        """.format(withinBracketsText, extractedMP4, extractedGIF)
                        comment.reply(message)
                    else:
                        comment.reply("No results were found")
                        
                # Store id in list
                posts_replied_to.append(comment.id)

                # Write updated list to file
                with open("posts_replied_to.txt", "w") as f:
                    for post_id in posts_replied_to:
                        f.write(post_id + "\n")
