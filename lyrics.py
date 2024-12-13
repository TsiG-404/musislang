from flask import Flask, request, render_template, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import os
import re
from urllib.parse import quote_plus

app = Flask(__name__)


'''
# Helper function to get metadata from YouTube
def get_metadata(youtube_url):
    try:
        ydl_opts = {'quiet': True, 'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            title = info.get('title', '').strip()
            uploader = info.get('uploader', '').strip()

            # Clean up title by removing anything inside parentheses
            title = re.sub(r'\(.*?\)', '', title).strip()

            return title, uploader
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None, None
'''
def get_metadata(youtube_url):
    try:
        ydl_opts = {'quiet': True, 'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            title = info.get('title', '').strip()
            uploader = info.get('uploader', '').strip()

            # Clean up title by removing anything inside parentheses
            title = re.sub(r'\(.*?\)', '', title).strip()

            # Extract artist from the title and save it to a file
            artist_name = None
            if '-' in title:
                artist_name = title.split('-')[0].strip()
            else:
                artist_name = title.split(' ')[0]

            # Save artist name to file
            if artist_name:
                with open("singer.txt", 'w') as file:
                    file.write(artist_name.strip())

            return title, uploader  # Return only title and uploader now

    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None, None





# Function to search Google for lyrics
def search_google_for_lyrics(title):
    try:
        search_query = quote_plus(f"{title} lyrics")
        results = search(search_query, num_results=10)
        for url in results:
            if any(site in url for site in ['genius.com', 'azlyrics.com', 'lyrics.com']):
                return url
        return None
    except Exception as e:
        print(f"Error searching Google: {e}")
        return None

# Function to extract lyrics from a URL


def extract_lyrics_from_url(song_url):
    try:
        response = requests.get(song_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        if "genius.com" in song_url:
            lyrics_divs = soup.find_all('div', {'data-lyrics-container': 'true'})
            lyrics_html = ''.join(str(div) for div in lyrics_divs)
            lyrics_text = '\n'.join(div.get_text(strip=True) for div in lyrics_divs)
            return lyrics_text, lyrics_html
        return None, None
    except Exception as e:
        print(f"Error extracting lyrics: {e}")
        return None, None
   



import os
from bs4 import BeautifulSoup
import os
from bs4 import BeautifulSoup

def save_lyrics_to_files(lyrics_text, lyrics_html, song_title, html_template_path="lyrics.html", placeholder_id="lyrics-container"):
    """
    Save lyrics and song title to a plain text file and update a specific part of an HTML file.

    - lyrics_text: Plain text of the lyrics.
    - lyrics_html: HTML-formatted lyrics.
    - song_title: Title of the song.
    - html_template_path: Path to the existing HTML file to update.
    - placeholder_id: ID of the <div> to update in the HTML file.
    """
    txt_file_path = "lyrics.txt"

    # Save lyrics and title as plain text
    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(f"Title: {song_title}\n\n{lyrics_text}")
    print(f"Lyrics saved as plain text to {txt_file_path}")

    try:
        # Check if the template HTML file exists
        if not os.path.exists(html_template_path):
            print(f"HTML template '{html_template_path}' not found. Creating a new one.")
            with open(html_template_path, "w", encoding="utf-8") as new_html_file:
                # Create a basic HTML template with a placeholder
                new_html_file.write(
                    f"<html><body><h1 id='song-title'></h1><div id='{placeholder_id}'></div></body></html>"
                )

        # Load the existing HTML file
        with open(html_template_path, "r", encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")

        # Update the song title
        title_placeholder = soup.find(id="song-title")
        if not title_placeholder:
            title_placeholder = soup.new_tag("h1", id="song-title")
            soup.body.insert(0, title_placeholder)
        title_placeholder.string = song_title  # Set the title text

        # Find the placeholder div by ID
        placeholder = soup.find(id=placeholder_id)
        if not placeholder:
            print(f"Error: No element with ID '{placeholder_id}' found.")
            return

        # Replace the content of the placeholder with the lyrics
        placeholder.clear()
        placeholder.append(BeautifulSoup(lyrics_html, "html.parser"))

        # Save the updated HTML back to the file
        with open(html_template_path, "w", encoding="utf-8") as html_file:
            html_file.write(str(soup))
        print(f"Lyrics successfully saved to {html_template_path}")
    except Exception as e:
        print(f"Error updating HTML file: {str(e)}")




def traslate(lyrics_text, html_template_path="lyrics.html", placeholder_id="translate"):
   
        # Load the existing HTML file
    with open(html_template_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    with open("translated.txt", "r", encoding="utf-8") as file:
            text_to_translate = file.read()

    # Update the song title
    title_placeholder = soup.find(id="translate")
    if not title_placeholder:
        title_placeholder = soup.new_tag("h1", id="translate")
        soup.body.insert(0, title_placeholder)
    title_placeholder.string = text_to_translate  # Set the title text

        # Save the updated HTML back to the file
    with open(html_template_path, "w", encoding="utf-8") as html_file:
        html_file.write(str(soup))
    print(f"Lyrics successfully saved to {html_template_path}")
    


# Route: Home
@app.route('/lyrics', methods=['POST'])
def lyrics():
    data = request.json
    youtube_url = data.get('url')

    if not youtube_url:
        return {"error": "YouTube URL is missing."}, 400

    # Get metadata from YouTube
    title, uploader = get_metadata(youtube_url)

    if not title:
        return {"error": "Failed to extract metadata from YouTube URL."}, 500

    # Search for lyrics using Google
    lyrics_url = search_google_for_lyrics(title)
    if not lyrics_url:
        return {"error": "No lyrics found for the song."}, 404

    # Extract lyrics from the found URL
    lyrics_text, lyrics_html = extract_lyrics_from_url(lyrics_url)
    if not lyrics_text:
        return {"error": "Failed to extract lyrics from the URL."}, 500

    # Save lyrics and title to files
    save_lyrics_to_files(
        lyrics_text,
        lyrics_html,
        song_title=title,  # Include the song title
        html_template_path="lyrics.html",
        placeholder_id="lyrics-container"
    )

    traslate(
        lyrics_text="translated.txt",
        html_template_path="lyrics.html",
        placeholder_id="translate"
        
    )


    

    return {
        "title": title,
        "uploader": uploader,
        "lyrics": lyrics_text,
        "saved_txt": "lyrics.txt",
        "saved_html": "lyrics.html"
    }, 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
