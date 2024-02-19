#!/bin/bash

# Define an array to hold the file names
files=()
# Define the directory path
dir="agent_conversations/JSON/"

# Loop through each file in the specified directory
for file in "$dir"*; do
    # Check if it's a regular file (not a directory or link, etc.)
    if [ -f "$file" ]; then
        # Add the file to the array, extracting just the filename if needed
        files+=("$(basename "$file")")
    fi
done


# Loop through the array of files
for file in "${files[@]}"; do
    # Execute your program here, using "$file" as an argument if needed
    # Replace 'your_program' with the actual program you want to run
    # And 'some_argument' with any arguments your program needs, if any
    python3 analysis_convo.py "$file"
    
    # For example, if you're counting words in each file using 'wc':
    # wc -w "$file"
done


