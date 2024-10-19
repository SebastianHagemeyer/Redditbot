import random
import subprocess


# Define placeholders for variables
subname = "SubredditNamePlaceholder"
topicList = "TopicListPlaceholder"
firstTitle = "TitlePlaceholder"
myPATH = "PathToYourFilesPlaceholder"

# Description template
desc = "Join us for the latest scoop on the funniest and most talked-about memes and drama from the popular subreddit /r/" + subname + ". \n" \
       + random.choice(["Today we're looking at:", "Today we're covering:", "In this episode, we're diving into the latest happenings, including:"]) \
       + "\n" + topicList + "\n Don't miss out on the laughs and join us for the latest memes and drama from the world of Reddit!"

# Write the description to a file
with open("desc.txt", "w", encoding='utf-8') as f:
    f.write(desc)

descfile = "desc.txt"
categ = "Entertainment"
tags = "reddit, news, " + subname

# Upload command with placeholders
#u = subprocess.call("youtube-upload --title=\" " + firstTitle + " \" --description-file=\"" + descfile + "\" --thumbnail \"" + myPATH + "\\0\\thumb.png\" --category=\"" + categ + "\" --tags=\"" + tags + "\" ./Out/final_output.mp4", shell=False)

import subprocess

command = [
    "python", "upload_video.py",
    "--file=./Out/final_output.mp4",
    "--title=Summer vacation in California",
    "--description=Had fun surfing in Santa Cruz",
    "--keywords=surfing,Santa Cruz",
    "--category=22",
    "--privacyStatus=private"
]

# Run the command
u=subprocess.call(command)

# Print the result of the upload command
print(u)
