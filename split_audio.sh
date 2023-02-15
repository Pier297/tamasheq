#!/bin/bash

# Set the input file
input_file="input.mp3"

# Get the length of the input file in seconds
length=$(ffprobe -i $input_file -show_entries format=duration -v quiet -of csv="p=0")

# Calculate the number of segments
num_segments=$(echo "$length/10" | bc)

# Split the input file
for i in $(seq 1 $num_segments);
do
    ffmpeg -i $input_file -ss $(((i-1)*10)) -t 10 -c copy "output/output_$i.mp3"
done