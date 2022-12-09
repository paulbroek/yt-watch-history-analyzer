"""watch_history.py.

Connect to YouTube API, 
retrieve recently watched videos

Run: 
    cd ~/repos/yt-watch-history-analyzer 
    ipy yt_watch_history_analyzer/scripts/watch_history.py


"""
import os
import pickle
import pprint
import sys
from typing import List, Optional

from apiclient.discovery import build  # type: ignore[import]
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from yt_watch_history_analyzer.settings import CONFIG_FILE, TOKEN_PICKLE_FILE
from yt_watch_history_analyzer.utils.misc import load_yaml

config = load_yaml(CONFIG_FILE)

# Set the authorization scope
# copy scopes from console.cloud.google.com/apis/credentials/consent/edit?project=YOUR_PROJECT_ID
SCOPES: List[str] = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtubepartner",
]

# Set the redirect URI
# REDIRECT_URI = "http://localhost"

creds: Optional[Credentials] = None
if os.path.exists(TOKEN_PICKLE_FILE):
    print("Loading credentials from pickle file...")
    with open(TOKEN_PICKLE_FILE, "rb") as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        print("Refreshing Access Token...")
        creds.refresh(Request())

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            config["client_secret_file"], scopes=SCOPES
        )
        flow.run_local_server(
            port=8080, prompt="consent", authorization_prompt_message=""
        )
        creds = flow.credentials

        # save OAuth credentials for the next run
        with open(TOKEN_PICKLE_FILE, "wb") as f:
            print("Saving credentials for future use..")
            pickle.dump(creds, f)

# use this when only using public API
# youtube_api = build("youtube", "v3", developerKey=config["api_key"])
# use this when only using private user data
youtube_api = build("youtube", "v3", credentials=creds)

myChannelId = config["my_channel_id"]
# cid="@coreyms"
# results = youtube_api.activities().list(channelId=cid, part="contentDetails").execute()

# get some activity, like subscribing to channels, ...
results = youtube_api.activities().list(mine=True, part="contentDetails").execute()

# get playlists, show them in alphabetical order
results = (
    youtube_api.playlists().list(mine=True, part="snippet", maxResults=50).execute()
)
pprint.pprint(sorted([a["snippet"]["title"] for a in results["items"]]))

# TODO: get my watch history playlist, how?
# see: https://developers.google.com/youtube/v3/docs
# results = youtube_api.channels().list(mine=True, part="contentDetails").execute()
# plId = "???"
# results = youtube_api.channels().playlistItems(mine=True, playlistId=plId, part="snippet").execute()
# or try a different approach, use Search endpoint, and filter for "completed": true
results = (
    youtube_api.search()
    .list(
        part="id",
        q="messi",
        type="video",
        fields="items(id)",
        eventType="completed",
        order="date",
    )
    .execute()
)

# -> Nope, the best approach still seem google Takeout. Automate the hell out of it and run daily job!


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
