# this a comment about extracting subtitles

import openai
import moviepy.editor as mp

# Load the video file using moviepy
video = mp.VideoFileClip("clip.mp4")

# Extract the audio from the video
audio = video.audio

# Convert the audio to a string representation
audio_string = str(audio.to_soundarray().tobytes())

# Initialize the OpenAI API client
openai.api_key = "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"

# Define the prompt for the GPT-3 model
prompt = "Please generate subtitles for the following audio clip:\n\n" + audio_string

# Use the OpenAI API to generate text with the prompt
completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# Get the generated text from the API response
generated_text = completions.choices[0].text

# Write the generated text to a .srt file
with open("subtitles.srt", "w") as file:
    file.write(generated_text)
