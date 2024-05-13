#!/bin/bash

# Check if the item name is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <item_name>"
    exit 1
fi

# Assign the first argument to the ITEM_NAME variable
ITEM_NAME="$1"

# Define the URL
URL="http://localhost:6000/generate"

# Define the JSON payload
JSON="{\"name\": \"$ITEM_NAME\"}"

# Make the POST request using curl
RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$JSON" "$URL")

# Check if the request was successful (status code 200)
if [ $? -eq 0 ]; then
    echo "Data generated successfully:"
    echo "$RESPONSE"
else
    echo "Error: Failed to generate data."
fi


