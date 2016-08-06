from video_requester import VideoRequest, Video
from emailer import Emailer

CHANNEL_ID = ''  # Insert channel ID
PLAYLIST_ID = ''  # Insert playlist ID
NUM_ITEMS = 20

mailer = Emailer('target_email', 'your_email', 'email_subject_line')  # Replace these with desired options

# Load all the previously checked videoIDs from the file
with open("video_log.txt", "a+") as f:
    already_checked = f.readlines()

# Request the videos and retrieve response in an array
requester = VideoRequest(CHANNEL_ID, PLAYLIST_ID, NUM_ITEMS)
requester.request_videos(NUM_ITEMS)
videos = requester.parse_response()

# Sort the videos with the corresponding query in the title into a new array
successes = []
for vid in videos:
    if "desired_query" in vid.title:
        successes.append(vid)

# Check that these videos have not already been notified for
for vid in successes:
    found = False
    if not already_checked:
        found = False

    for line in already_checked:
        if vid.video_id in line:
            found = True
            break

    # If the video has not already been checked, add it to the file and send an email notification
    if not found:
        mailer.send_email(vid.video_id, vid.title)
        with open("video_log.txt", "a+") as f:
            f.write(vid.video_id + " " + vid.title + '\n')
