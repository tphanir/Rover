#!/bin/bash

# File to monitor
FILE="VoiceNav/data.txt"

# Check if the file exists
if [[ ! -f "$FILE" ]]; then
  echo "File '$FILE' does not exist."
  exit 1
fi

# Continuously print the file's content
while true; do
  clear # Clears the terminal for each print
  cat "$FILE"
  sleep 2 # Wait 2 seconds before updating (adjust as needed)
done

