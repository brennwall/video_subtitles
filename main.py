import openai
import moviepy.editor as mp

# Load the video file using moviepy
print('Loading video file with moviepy...')
video = mp.VideoFileClip("clip.mp4")

# Extract the audio from the video
print("Extracting audio from video...")
audio = video.audio

# Convert the audio to a string representation
print("Converting audio to string...")
audio_string = str(audio.to_soundarray().tobytes())

# Split the audio string into smaller chunks
chunk_size = 2200
num_chunks = (len(audio_string) // chunk_size) + 1
audio_chunks = [audio_string[i:i+chunk_size] for i in range(0, len(audio_string), chunk_size)]

# Initialize the OpenAI API client
openai.api_key = "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"

# Define the prompt for the GPT-3 model
prompts = ["Please generate subtitles for the following audio clip:\n\n" + chunk for chunk in audio_chunks]

# Use the OpenAI API to generate text with the prompts
generated_text = ""
for i, prompt in enumerate(prompts):
    print("Generating text for chunk " + str(i) + " of " + str(num_chunks) + "...")
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=chunk_size,
        n=1,
        stop=None,
        temperature=0.5,
    )
    generated_text += completions.choices[0].text


# Write the generated text to a .srt file
with open("subtitles.srt", "w") as file:
    file.write(generated_text)