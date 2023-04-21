import os
import requests
import json

# Set up the ChatGPT API endpoint and your API key
endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
api_key = "YOUR_API_KEY_HERE"

# Define a function to get the book name from a file name using ChatGPT


def get_book_name(filename):
    prompt = f"Extract the book name from the file name '{filename}'."
    data = {
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.5
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(endpoint, headers=headers, json=data)
    book_name = response.json()["choices"][0]["text"].strip()
    return book_name


# Define the folder to search for PDF files in
folder_path = "path/to/folder"

# Loop through all the files in the folder and its subfolders
for root, dirs, files in os.walk(folder_path):
    for file in files:
        # Check if the file is a PDF file
        if file.lower().endswith(".pdf"):
            # Get the book name from the file name using ChatGPT
            book_name = get_book_name(file)
            # Rename the file with the book name
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, f"{book_name}.pdf")
            os.rename(file_path, new_file_path)
            # Print a message to show that the file has been renamed
            print(f"Renamed {file_path} to {new_file_path}")
