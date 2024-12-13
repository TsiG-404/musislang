import os
import subprocess
import yt_dlp
from flask import Flask, render_template_string
from spleeter.separator import Separator
import tensorflow as tf

'''
# Set TensorFlow settings
tf.config.optimizer.set_jit(True)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)
'''

def read_link(file_name="link.txt"):
    try:
        with open(file_name, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return None


# Function to resample the audio
def resample_audio(input_file, output_file, sample_rate=22050, channels=1):
    try:
        command = [
            "ffmpeg",
            "-i", input_file,          
            "-ar", str(sample_rate),   
            "-ac", str(channels),      
            "-y",                      
            output_file
        ]
        subprocess.run(command, check=True)
        print("OK!!!!")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during resampling: {e}")
        return None

# Function to separate vocals and accompaniment
def separate_audio(input_file, output_dir="output"):
    try:
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(input_file, output_dir)
        
        # Get the paths to the separated files
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        vocal_file = os.path.join(output_dir, base_name, "vocals.wav")
        beat_file = os.path.join(output_dir, base_name, "accompaniment.wav")
        print("OK2!!!!!")
        
        return vocal_file, beat_file
    except Exception as e:
        print(f"Error during separation: {e}")
        return None, None

# Function to download audio from YouTube
def download_audio(link, output_file="audio"):
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

# Function to convert WAV to MP3
def convert_to_mp3(wav_file, mp3_file):
    try:
        subprocess.run(["ffmpeg", "-i", wav_file, "-q:a", "0", mp3_file, "-y"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting WAV to MP3: {e}")

# Function to create an HTML page displaying the separated tracks
def create_html(vocal_file, beat_file, output_file="separation.html"):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Separation Results</title>
        
            <link rel="stylesheet" href="css/separation.css">
    
    
    </head>
    <body>
        <h1>Separated Audio</h1>
        
        <h2>Vocals</h2>
        
        <div id="m">
        <audio controls>
            <source src="{vocal_file}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <h2>Instruments</h2>
        <audio controls>
            <source src="{beat_file}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        </div>
        <div class="button-container">
<form action="/paraphrased" method="POST">
<button type="submit">grammar</button>
</form>
<form action="/map" method="POST">
<button type="submit">Origin</button>
</form>
<form action="/lyrics3" method="POST">
<button type="submit">lyrics</button>
</form>
<form action="http://127.0.0.1:5002" method="GET">
<button type="submit">Karaoke</button>
</form>
</div>

    </body>
    </html>
    """
    try:
        with open(output_file, "w") as file:
            file.write(html_template)
        print(f"HTML file created: {output_file}")
    except Exception as e:
        print(f"Error creating HTML: {e}")




from bs4 import BeautifulSoup



# Main function to orchestrate the process
def main():
    link = read_link()
    if not link:
        return

    print("Downloading audio...")
    audio_file = download_audio(link)
    if not audio_file:
        return

    print("Resampling audio...")
    resampled_file = resample_audio(audio_file, "audio_downsampled.wav")
    if not resampled_file:
        return

    print("Separating audio...")
    vocal_wav, beat_wav = separate_audio(resampled_file)
    if not (vocal_wav and beat_wav):
        return

    print("Converting WAV to MP3...")
    convert_to_mp3(vocal_wav, "static/vocal.mp3")
    convert_to_mp3(beat_wav, "static/beat.mp3")

    print("Creating HTML file...")
    create_html("static/vocal.mp3", "static/beat.mp3")

    print("Process completed successfully!")

if __name__ == "__main__":
    main()
    
