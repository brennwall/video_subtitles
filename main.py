from pydub import AudioSegment
import whisper
from moviepy.editor import VideoFileClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

def convert_to_srt(result):
    # Initialize the counter for the srt file's subtitle number
    subtitle_num = 1

    # Open a file for writing
    with open("clip.srt", "w") as file:
        # Iterate over each segment in the result
        for segment in result['segments']:
            # Write the subtitle number
            file.write(str(subtitle_num) + "\n")
            
            # Write the start and end times for the segment
            start_time = str(int(segment['start'] // 60)).zfill(2) + ":" + str(int(segment['start'] % 60)).zfill(2) + "," + str(int((segment['start'] % 1) * 1000)).zfill(3)
            end_time = str(int(segment['end'] // 60)).zfill(2) + ":" + str(int(segment['end'] % 60)).zfill(2) + "," + str(int((segment['end'] % 1) * 1000)).zfill(3)
            file.write(start_time + " --> " + end_time + "\n")
            
            # Write the text for the segment
            file.write(segment['text'] + "\n\n")
            
            # Increment the subtitle number
            subtitle_num += 1


# Load the mp4 file
sound = AudioSegment.from_file("clip.mp4", format="mp4")

# Save the mp3 file
sound.export("clip.mp3", format="mp3")

model = whisper.load_model("base")
result = model.transcribe('clip.mp3')
convert_to_srt(result)


# Load the video file
video = VideoFileClip("clip.mp4")

# Load the subtitle file
subtitles = open("clip.srt").read()

# Create the subtitle clip
subtitle_clip = TextClip(subtitles, fontsize=30, color='white')

# Combine the video and subtitle clips
final_clip = CompositeVideoClip([video, subtitle_clip.set_pos(("center", 550))])

# # Save the final clip
final_clip.duration = video.duration
final_clip.write_videofile("final_video.mp4")
