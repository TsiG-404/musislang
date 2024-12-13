import yt_dlp
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from requests.exceptions import RequestException
from urllib.parse import quote_plus
import os

# Define the function to get metadata from YouTube URL
import re

def get_metadata(youtube_url):
    try:
        ydl_opts = {'quiet': True, 'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            title = info.get('title')
            uploader = info.get('uploader')

            # Remove anything inside parentheses (including the parentheses)
            title = re.sub(r'\(.*?\)', '', title).strip()  # Regex to remove text inside parentheses

            print(f"DEBUG: Title - {title}, Uploader - {uploader}")
            return title, uploader
    except Exception as e:
        print(f"Error extracting metadata: {str(e)}")
        return None, None


# Function to search Google for the song title and get the first relevant URL
def search_google_for_lyrics(title):
    search_query = quote_plus(title + " lyrics")  # Ensure "lyrics" is part of the query
    try:
        # Perform the Google search (limit results to 10)
        result_urls = search(search_query, num_results=10)
        
        # Look for a URL that likely leads to lyrics (heuristic: check if the URL contains 'lyrics')
        for url in result_urls:
            if 'lyrics' in url.lower() and ('azlyrics' in url.lower() or 'genius' in url.lower() or 'lyrics.com' in url.lower()):
                print(f"DEBUG: Found lyrics URL - {url}")
                return url
        
        print("No relevant lyrics results found.")
        return None
    except Exception as e:
        print(f"Error searching Google: {str(e)}")
        return None

# Function to extract lyrics from a webpage
def extract_lyrics_from_url(song_url):
    lyrics = []  # List to collect lyrics from multiple containers
    try:
        response = requests.get(song_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Genius lyrics extraction using 'data-lyrics-container' attribute
        if "genius.com" in song_url:
            # Look for all divs with the 'data-lyrics-container' attribute
            lyrics_divs = soup.find_all('div', {'data-lyrics-container': 'true'})
            
            # Iterate over all found containers and collect the text content
            for lyrics_div in lyrics_divs:
                lyrics.append(lyrics_div.get_text(strip=True))  # Extract plain text

        # Prepare the plain text and HTML version of the lyrics
        lyrics_text = '\n'.join(lyrics)  # Plain text, newlines between lyrics
        lyrics_html = "<html><body><h1>Lyrics</h1>" + "<br>".join(lyrics) + "</body></html>"  # HTML with <br> between lyrics
        
        return lyrics_text, lyrics_html
    except RequestException as e:
        print(f"Error accessing the lyrics page: {str(e)}")
        return None, None

# Function to save the HTML and plain text versions of the lyrics
def save_lyrics(lyrics_text, lyrics_html, song_title):
    if lyrics_text:
        # Save the plain text version
        txt_file_path = f"lyrics.txt"
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(lyrics_text)
        print(f"Lyrics saved as plain text to {txt_file_path}")
    
    if lyrics_html:
        # Save the HTML version
        html_file_path = f"lyrics.html"
        with open(html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(lyrics_html)
        print(f"Lyrics saved as HTML to {html_file_path}")

# Example usage
def main():
    youtube_url = "https://www.youtube.com/watch?v=ucVUEmjKsko"  # Replace with actual YouTube URL
    
    title, uploader = get_metadata(youtube_url)
    if title:
        lyrics_url = search_google_for_lyrics(title)
        if lyrics_url:
            lyrics_text, lyrics_html = extract_lyrics_from_url(lyrics_url)
            if lyrics_text:
                save_lyrics(lyrics_text, lyrics_html, title)

if __name__ == "__main__":
    main()
