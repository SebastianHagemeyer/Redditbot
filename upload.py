import os
import random
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import httplib2
from googleapiclient.http import MediaFileUpload

# Replace placeholders with actual values
subname = "SubredditNamePlaceholder"
topicList = "TopicListPlaceholder"
firstTitle = "TitlePlaceholder"
myPATH = "C:\Automate\RedditBot"
video_file = "./Out/final_output.mp4"  # Your video file
thumbnail_file = os.path.join(myPATH, "0", "thumb.png")

# Description generation logic
desc = (
    "Join us for the latest scoop on the funniest and most talked-about memes and drama from the popular subreddit /r/" 
    + subname + ". \n" 
    + random.choice([
        "Today we're looking at:", 
        "Today we're covering:", 
        "In this episode, we're diving into the latest happenings, including:"
    ]) 
    + "\n" + topicList 
    + "\n Don't miss out on the laughs and join us for the latest memes and drama from the world of Reddit!"
)

# YouTube API setup
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "C:/Users/Sebastian/.client_secrets.json "  # Replace with the path to your client_secrets.json file

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, video_file, title, description, tags, category_id, thumbnail_file):
    # Create request body for the video
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags.split(", "),
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": "public"
        }
    }
    
    # Upload the video
    media_file = MediaFileUpload(video_file)
    video_upload_response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    ).execute()

    # Set thumbnail
    youtube.thumbnails().set(
        videoId=video_upload_response["id"],
        media_body=thumbnail_file
    ).execute()

    print(f"Video uploaded successfully: https://youtu.be/{video_upload_response['id']}")

def main():
    youtube = get_authenticated_service()

    # Define the tags and category (Entertainment is category ID 24 on YouTube)
    tags = "reddit, news, " + subname
    category_id = "24"

    # Upload the video
    upload_video(youtube, video_file, firstTitle, desc, tags, category_id, thumbnail_file)

if __name__ == "__main__":
    main()
