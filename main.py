from pydub import AudioSegment
import whisper
import ffmpeg
import os


def convert_to_srt(result, file):
    # Initialize the counter for the srt file's subtitle number
    subtitle_num = 1

    # Open a file for writing
    with open(file, "w") as file:
        # Iterate over each segment in the result
        for segment in result['segments']:
            # Write the subtitle number
            file.write(str(subtitle_num) + "\n")
            
            # Write the start and end times for the segment
            start_time = str(int(segment['start'] // 3600)).zfill(2) + ":" + str(int((segment['start'] % 3600) // 60)).zfill(2) + ":" + str(int(segment['start'] % 60)).zfill(2) + "," + str(int((segment['start'] % 1) * 1000)).zfill(3)
            end_time = str(int(segment['end'] // 3600)).zfill(2) + ":" + str(int((segment['end'] % 3600) // 60)).zfill(2) + ":" + str(int(segment['end'] % 60)).zfill(2) + "," + str(int((segment['end'] % 1) * 1000)).zfill(3)

            file.write(start_time + " --> " + end_time + "\n")
            
            # Write the text for the segment
            file.write(segment['text'] + "\n\n")
            
            # Increment the subtitle number
            subtitle_num += 1

INPUT_VIDEO_FILE = "clip.mp4"
INPUT_AUDIO_FILE = "audio.mp3"
SUBTITLES_FILE = "subtitles.srt"
OUTPUT_VIDEO_WITH_SUBTITLES_FILE = 'video_with_subtitles.mp4'
OUTPUT_VIDEO_WITH_AUDIO_AND_SUBTITLES_FILE = "final_video.mp4"

sound = AudioSegment.from_file(INPUT_VIDEO_FILE, format="mp4")
sound.export(INPUT_AUDIO_FILE, format="mp3")

model = whisper.load_model("base")
result = model.transcribe(INPUT_AUDIO_FILE)
convert_to_srt(result, SUBTITLES_FILE)


ffmpeg .input(INPUT_VIDEO_FILE) .filter('subtitles', SUBTITLES_FILE) .output(OUTPUT_VIDEO_WITH_SUBTITLES_FILE).run()

input_video = ffmpeg.input(OUTPUT_VIDEO_WITH_SUBTITLES_FILE)
input_audio = ffmpeg.input(INPUT_AUDIO_FILE)

ffmpeg.concat(input_video, input_audio, v=1, a=1).output(OUTPUT_VIDEO_WITH_AUDIO_AND_SUBTITLES_FILE).run()

os.remove(INPUT_AUDIO_FILE)
os.remove(SUBTITLES_FILE)
os.remove(OUTPUT_VIDEO_WITH_SUBTITLES_FILE)