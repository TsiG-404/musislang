import os
import time
import threading
from flask import Flask, render_template, jsonify, request, send_file, make_response
import pygame
import yt_dlp
from spleeter.separator import Separator  # Ensure Spleeter is installed
from threading import Lock

# Flask app setup
app = Flask(__name__, template_folder='.')

# Global variables
current_timestamp = 0
lyrics = []
is_playing = False
start_time = 0
pause_time = 0
is_playing_lock = Lock()

def set_is_playing(value):
    global is_playing
    with is_playing_lock:
        is_playing = value

def get_is_playing():
    with is_playing_lock:
        return is_playing

@app.route('/')
def show_page():
    return render_template('song.html')

@app.route('/control', methods=['POST'])
def control_music():
    global start_time, pause_time
    action = request.json.get("action")
    print(f"DEBUG: Received action: {action}")
    if action == "play":
        if not get_is_playing():
            set_is_playing(True)
            threading.Thread(target=play_music, args=("song.mp3",)).start()
            threading.Thread(target=sync_lyrics, daemon=True).start()
    elif action == "pause":
        if get_is_playing():
            pygame.mixer.music.pause()
            pause_time = time.time()
            set_is_playing(False)
            print("DEBUG: Music paused.")
    elif action == "resume":
        if not get_is_playing():
            pygame.mixer.music.unpause()
            start_time += time.time() - pause_time
            set_is_playing(True)
            print("DEBUG: Music resumed.")
    return jsonify({"status": "success"})

@app.route('/lyrics2')
def get_lyrics():
    global lyrics, current_timestamp
    output = ""
    print(f"DEBUG: Current timestamp: {current_timestamp}")
    for timestamp, text in lyrics:
        if current_timestamp > timestamp:
            output += f'<div class="lyrics passed">{text}</div>'
        elif current_timestamp == timestamp:
            output += f'<div class="lyrics current">{text}</div>'
        else:
            output += f'<div class="lyrics upcoming">{text}</div>'
    print(f"DEBUG: Lyrics output: {output}")
    return output

def play_music(music_file):
    global start_time
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    start_time = time.time()
    set_is_playing(True)
    print("DEBUG: Music started, is_playing set to True.")

def sync_lyrics():
    global start_time, current_timestamp
    print("DEBUG: Starting sync_lyrics loop.")
    while get_is_playing():
        current_timestamp = int(time.time() - start_time)
        print(f"DEBUG: Updated timestamp: {current_timestamp}")
        time.sleep(0.5)
    print("DEBUG: Exiting sync_lyrics loop.")

def format_lyrics(input_file, output_file, words_per_line=5, seconds_per_line=3):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lyrics = []
    timestamp = 0

    for line in lines:
        if line.strip():
            words = line.split()
            for i in range(0, len(words), words_per_line):
                chunk = " ".join(words[i:i + words_per_line])
                minutes, seconds = divmod(timestamp, 60)
                formatted_lyrics.append(f"[{minutes:02}:{seconds:02}] {chunk}")
                timestamp += seconds_per_line

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(formatted_lyrics))

    print(f"Formatted lyrics saved to {output_file}")

def load_lyrics(file_path):
    global lyrics
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                parts = line.strip().split(']')
                if len(parts) == 2:
                    time_part = parts[0][1:]
                    lyric_part = parts[1]
                    minutes, seconds = map(int, time_part.split(':'))
                    timestamp = minutes * 60 + seconds
                    lyrics.append((timestamp, lyric_part))
    lyrics.sort()

def read_link(file_name="link.txt"):
    try:
        with open(file_name, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return None

def download_audio(link, output_file="song"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f"{output_file}.%(ext)s"
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return f"{output_file}.mp3"
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

@app.route('/kara', methods=['GET', 'POST'])
def kara():
    global lyrics, current_timestamp
    lyrics.clear()
    
    link = read_link()
    print("Downloading audio...")
    audio_file = download_audio(link)
    format_lyrics("lyrics.txt", "raw_lyrics.txt")
    time.sleep(5)
    load_lyrics("raw_lyrics.txt")
    print("Lyrics and audio ready.")
    return send_file("song.html", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, threaded=True, port=5002)
