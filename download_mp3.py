import requests
from bs4 import BeautifulSoup
import re
import os

url = "https://www.studiotamani.org/125169-les-titres-du-17-janvier-2023-soir"

# Download the web page
response = requests.get(url)
content = response.content

folder = "original"

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(content, 'html.parser')

# Find all mp3 file links on the page
links = soup.find_all("a", href=re.compile(".*\.mp3$"))

# Download each mp3 file
for link in links:
    mp3_url = link["href"]
    mp3_response = requests.get(mp3_url)
    mp3_content = mp3_response.content
    filename = mp3_url.split("/")[-1]
    filename = f"{folder}/{filename}"
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.mkdir(folder)
    with open(filename, "wb") as f:
        f.write(mp3_content)
    print(f"Downloaded {filename}")