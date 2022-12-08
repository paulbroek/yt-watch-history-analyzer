"""watch_history.py.

Connect to YouTube API, 
retrieve recently watched videos

Run: 


"""
import sys
from pathlib import Path

from apiclient.discovery import build  # type: ignore[import]
from google.oauth2.credentials import Credentials, UserAccessTokenCredentials
from oauth2client import client, file, tools  # type: ignore[import]
# from google.oauth2.flow import Flow
from yt_watch_history_analyzer import config as config_dir
from yt_watch_history_analyzer.utils.misc import load_yaml

cfgFile = "/home/paul/repos/yt-watch-history-analyzer/yt_watch_history_analyzer/config/config.yaml"

config = load_yaml(cfgFile)

# Set the authorization scope
SCOPES = "https://www.googleapis.com/auth/youtube.force-ssl"

# Set the redirect URI
REDIRECT_URI = "http://localhost"

# DEPRECIATED?
# Create the OAuth flow object
# flow = Flow.from_client_secrets_file(
#     client_secrets_file=config["client_secret_file"],
#     scope=SCOPE,
#     redirect_uri=REDIRECT_URI
# )
flow = client.flow_from_clientsecrets(config["client_secret_file"], SCOPES)

# for personal data, you need to create a credentials object
# TODO: pass scopes needed for private youtube data?
# scopes = None
# creds = Credentials.from_authorized_user_info(
#     info={"client_id": config["client_id"], "client_secret": config["client_secret"]},
#     scopes=scopes,
# )
# creds = Credentials(client_id=config["client_id"], client_secret=config["client_secret"])
# creds = Credentials.from_authorized_user_file("/home/paul/Downloads/google-services.json")
# youtube_api = build("youtube", "v3", developerKey=config["api_key"])
youtube_api = build("youtube", "v3", credentials=creds)

# Replace "YOUR_QUERY" with your search query (e.g. "videos I watched this week")
results = (
    youtube_api.search()
    .list(part="id", q="messi", type="video", fields="items(id)")
    .execute()
)

CHANNEL_ID = "SoothingRelaxation"

sys.exit()


# Replace "YOUR_VIDEO_ID" with the ID of the video you want to retrieve information for
video_info = (
    youtube_api.videos()
    .list(
        part="contentDetails",
        id="YOUR_VIDEO_ID",
        fields="items(contentDetails(duration))",
    )
    .execute()
)

total_time_watched = 0

# Loop through the list of videos that you have watched
for video in results["items"]:
    # Retrieve the duration of each video
    duration = video_info["items"][0]["contentDetails"]["duration"]

    # Parse the duration of the video into hours, minutes, and seconds
    hours, minutes, seconds = map(int, duration.split(":"))

    # Convert the duration of the video into seconds
    seconds_watched = (hours * 3600) + (minutes * 60) + seconds

    # Add the duration of the video to the total time watched
    total_time_watched += seconds_watched

# Convert the total time watched into hours, minutes, and seconds
hours_watched = total_time_watched // 3600
minutes_watched = (total_time_watched % 3600) // 60
seconds_watched = total_time_watched % 60
