import youtube
# from googleapiclient.discovery import build
from apiclient.discovery import build  # type: ignore[import]

# from google.oauth2.credentials import Credentials

# Replace "YOUR_API_KEY" with your actual API key
# creds = Credentials.from_authorized_user_info(info={"apiKey": "YOUR_API_KEY"})

youtube_api = build("youtube", "v3", developerKey=api_key)

# Replace "YOUR_QUERY" with your search query (e.g. "videos I watched this week")
results = youtube.search().list(
   	part="id",
    q="YOUR_QUERY",
    type="video",
    fields="items(id)"
).execute()

# Replace "YOUR_VIDEO_ID" with the ID of the video you want to retrieve information for
video_info = youtube.videos().list(
    part="contentDetails",
    id="YOUR_VIDEO_ID",
    fields="items(contentDetails(duration))"
).execute()

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
