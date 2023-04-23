import cloudinary.uploader
import cloudinary.api
import re
import io
from pytube import YouTube
from twilio.rest import Client

# Set up the Twilio client using your account SID and auth token
account_sid = 'AC8d5920728a89dac8da9113c077ccac20'
auth_token = '9fc14b0e42ea8d238c56232ac0ecc424'
client = Client(account_sid, auth_token)

# Retrieve the last message from a specific WhatsApp conversation
messages = client.messages.list(from_='whatsapp:+14155238886',)
if messages:
    last_message = messages[0].body
    Mlink = last_message 
    print(Mlink)
else:
    print("No messages found.")

# Extract the YouTube video URL or short URL from the message
def extract_youtube_url(message):
    pattern = r'(https?://)?(www\.)?(youtube|youtu\.be)/(watch\?v=|embed/|v/)?[\w\-]{11}'
    match = re.search(pattern, message)
    if match:
        video_id = match.group().split('/')[-1]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        pattern = r'(https?://)?(www\.)?youtube\.com/shorts/[\w\-]{11}'
        match = re.search(pattern, message)
        if match:
            return match.group()
        else:
            dump = client.messages.list(to='whatsapp:+14155238886', limit=1)[0]
            message = client.messages.create(
                body="Send me a video URL",
                from_='whatsapp:+14155238886',
                to=dump._from
            )

# Set up Cloudinary credentials
cloudinary.config(
    cloud_name="dwj7tznit",
    api_key="678549699212321",
    api_secret="b0QPfC_oXWUluc6Mt2Y92YzNK6E"
)

# Download the video and upload it to Cloudinary
youtube_url = extract_youtube_url(Mlink)
print(youtube_url)
if youtube_url:
    
    # Create a YouTube object with the video URL
    youtube = YouTube(youtube_url)
    print(youtube)
    # Get the first stream with the 360 resolution
    stream = youtube.streams.filter(res='360p').first()
    # Open a bytes IO object and download the video stream to it
    video_stream = io.BytesIO()
    stream.stream_to_buffer(video_stream)
    # Reset the IO object to the beginning
    video_stream.seek(0)
    # Upload the video stream to Cloudinary
    upload_result = cloudinary.uploader.upload(
        video_stream,
        resource_type="video",
        folder="Mythesis_vedios",
        public_id=youtube.video_id,
        overwrite=True
    )

    if 'secure_url' in upload_result:
        video_url = upload_result['secure_url']
        print(f"Video uploaded to Cloudinary successfully! URL: {video_url}")
        # Send a message with the Cloudinary URL of the video
        dump = client.messages.list(to='whatsapp:+14155238886', limit=1)[0]
        # Print details of the message
        print("From:", dump._from)
        # Send WhatsApp message with video URL
        message = client.messages.create(
            body="Here is your video: " + video_url,
            from_='whatsapp:+14155238886',
            to=dump._from
        )
    else:
        print("Failed to upload video to Cloudinary")
        # Send a message if video upload fails
        dump = client.messages.list(to='whatsapp:+14155238886', limit=1)[0]
        message = client.messages.create(
            body="Failed to upload the video.",
            from_='whatsapp:+14155238886',
            to=dump._from
        )





