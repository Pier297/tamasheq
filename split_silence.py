import subprocess
import re
import os

# Set the input file
input_file = "Journal_tas-17012023.mp3"
db = 30
duration = 0.2
output_dir = "silence"

# Check if the output directory exists, if not create it; otherwise ask the user if they want to overwrite the directory
try:
    os.mkdir(output_dir)
except FileExistsError:
    overwrite = input("Output directory already exists, do you want to overwrite it? (y/n): ")
    if overwrite == "y":
        print("Overwriting...")
        for file in os.listdir(output_dir):
            os.remove(f"{output_dir}/{file}")
    else:
        print("Exiting...")
        exit()

result = subprocess.run(['ffmpeg', '-i', input_file, '-af', f'silencedetect=noise=-{db}dB:d={duration}', '-f', 'null', '-'], capture_output=True, text=True)
output = result.stderr

# Extract the silence start and end times
start_times = re.findall(r'silence_start: (\d+\.\d+)', output)
durations = re.findall(r'silence_duration: (\d+\.\d+)', output)


# Split the input file so that we split on silence
current_position = 0
audio_durations = []
for i in range(len(start_times)):
    start_time = float(start_times[i])
    duration = float(durations[i])
    end_time = start_time + duration
    subprocess.run(['ffmpeg', '-i', input_file, '-ss', str(current_position), '-to', str(start_time), '-c', 'copy', f'{output_dir}/output_{i}.mp3'])
    audio_durations.append(start_time - current_position)
    current_position = end_time

# Copy the last part of the file
subprocess.run(['ffmpeg', '-i', input_file, '-ss', str(current_position), '-c', 'copy', f'{output_dir}/output_{len(start_times)}.mp3'])

print("Created {} files".format(len(start_times) + 1))
print("Average audio duration: {} seconds".format(sum(audio_durations) / len(audio_durations)))
print("Max audio duration: {} seconds".format(max(audio_durations)))
print("Min audio duration: {} seconds".format(min(audio_durations)))
print("Index with < 0 audio duration: {}".format([i for i, x in enumerate(audio_durations) if x < 0]))