from flask import Flask, request, render_template, send_file, jsonify
import requests
import os
import subprocess
from bs4 import BeautifulSoup

app = Flask(__name__)
SECOND_SCRIPT_URL = "http://127.0.0.1:5001/lyrics"


#edo!!!
THIRD_SCRIPT_URL = "http://127.0.0.1:5002/kara"  # URL of the secondary script

def open_lyrics_script():
    script_path = "lyrics.py"  # Adjust the path if needed
    subprocess.Popen(["cmd", "/k", f"python {script_path}"], shell=True)

@app.route('/')
def index():
    #open_lyrics_script()
    return render_template('index.html')  # HTML form to input YouTube URL

@app.route('/lyrics', methods=['POST'])
def lyrics():
    youtube_url = request.form.get('url')
    if not youtube_url:
        return "YouTube URL is missing.", 400

    lang = request.form.get('language')
    with open("link.txt", 'w') as file1, open("lang.txt", 'w') as file2:
        file1.write(youtube_url)
        file2.write(lang)

    try:
        response = requests.post(SECOND_SCRIPT_URL, json={'url': youtube_url})
        if response.status_code == 200:
            subprocess.run(['python', 'translate.py'])
            subprocess.run(['python', 'artis.py'])
            subprocess.run(['python', 'map.py'])
            subprocess.run(['python', 'para.py'])

            if os.path.exists("lyrics.html"):
                subprocess.run(['python', 'lyrics.py', 'translate', 'translated.txt', 'lyrics.html', 'translate'])
                #subprocess.Popen(["cmd", "/k", "python kara.py"], shell=True)
                #subprocess.Popen(["cmd", "/k", "python kara.py"], shell=True)
                #subprocess.Popen(["python", "kara.py"], shell=True)


                response = requests.post(THIRD_SCRIPT_URL)
                #subprocess.Popen(["cmd", "/k", "python kara.py"], shell=True)


    
                return send_file("lyrics.html", as_attachment=False)
            else:
                return "Lyrics file not found.", 500
        else:
            return f"Failed to process URL. Error: {response.text}", response.status_code
    except Exception as e:
        return f"Error communicating with the second script: {str(e)}", 500

@app.route('/lyrics2', methods=['POST'])
def lyrics2():
    paraphrased_file_path = "song.html"
    if os.path.exists(paraphrased_file_path):
        return send_file(paraphrased_file_path, as_attachment=False)
    else:
        return "Song file not found.", 501

@app.route('/paraphrased', methods=['POST'])
def paraphrased():
    paraphrased_file_path = "paraphrased.html"
    if os.path.exists(paraphrased_file_path):
        return send_file(paraphrased_file_path, as_attachment=False)
    else:
        return "Paraphrased file not found.", 501

@app.route('/translate', methods=['POST'])
def translate():
    paraphrased_file_path = "translated.html"
    if os.path.exists(paraphrased_file_path):
        return send_file(paraphrased_file_path, as_attachment=False)
    else:
        return "Translated file not found.", 502
    



'''
@app.route('/separation', methods=['POST'])
def separation():
    subprocess.run(['python', 'song.py'])
    paraphrased_file_path = "separation.html"
    if os.path.exists(paraphrased_file_path):
        return send_file(paraphrased_file_path, as_attachment=False)
    else:
        return "Translated file not found.", 502
    
'''

from flask import Flask, send_file, render_template_string
import subprocess
import os


'''

@app.route('/separation', methods=['POST'])
def separation():
    try:
        # Run the separation script
        subprocess.run(['python', 'song.py'], check=True)

        # File paths
        vocal_file = "vocal.mp3"
        beat_file = "beat.mp3"
        html_file_path = "separation.html"

        # Ensure files exist
        if not (os.path.exists(vocal_file) and os.path.exists(beat_file)):
            return "One or more MP3 files are missing.", 404
        if not os.path.exists(html_file_path):
            return "HTML file not found.", 404

        # Serve the HTML file
        return send_file(html_file_path, as_attachment=False)

    except subprocess.CalledProcessError:
        return "Error while processing the separation script.", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500
'''
from flask import Flask, send_file, render_template_string
import subprocess
import os
import shutil

'''

@app.route('/separation', methods=['POST'])
def separation():
    try:
        # Run the separation script
        subprocess.run(['python', 'song.py'], check=True)

        # File paths
        vocal_file = "vocal.mp3"
        beat_file = "beat.mp3"
        html_file_path = "separation.html"

        # Ensure files exist
        if not (os.path.exists(vocal_file) and os.path.exists(beat_file)):
            return "One or more MP3 files are missing.", 404
        if not os.path.exists(html_file_path):
            return "HTML file not found.", 404

        # Move MP3 files to the static folder
        static_folder = os.path.join(os.getcwd(), "static")
        os.makedirs(static_folder, exist_ok=True)
        shutil.move(vocal_file, os.path.join(static_folder, vocal_file))
        shutil.move(beat_file, os.path.join(static_folder, beat_file))

        # Read and modify the HTML file dynamically
        with open(html_file_path, 'r') as file:
            html_content = file.read()

        # Inject the correct MP3 file paths into the HTML
        updated_html = html_content.format(
            vocal_file=f"/static/{vocal_file}",
            beat_file=f"/static/{beat_file}"
        )

        # Serve the updated HTML
        return render_template_string(updated_html)

    except subprocess.CalledProcessError:
        return "Error while processing the separation script.", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500
'''
@app.route('/separation', methods=['POST'])
def separation():
    print("Separation route triggered!")
    try:
        # Run the separation script
        subprocess.run(['python', 'song.py'], check=True)
        print("song.py script executed successfully.")

        # File paths
        vocal_file = "vocal.mp3"
        beat_file = "beat.mp3"
        html_file_path = "separation.html"
        style="separation.css"

        # Check if files exist
        if not os.path.exists(vocal_file):
            print("vocal.mp3 not found.")
            return "vocal.mp3 is missing.", 404
        if not os.path.exists(beat_file):
            print("beat.mp3 not found.")
            return "beat.mp3 is missing.", 404
        if not os.path.exists(html_file_path):
            print("separation.html not found.")
            return "separation.html is missing.", 404

        print("All files found. Preparing response.")

        # Serve the HTML file
        with open(html_file_path, 'r') as file:
            html_content = file.read()

        # Inject MP3 paths
        updated_html = html_content.format(
            vocal_file=vocal_file,
            beat_file=beat_file,
            style=style
        )
        return render_template_string(updated_html)

    except subprocess.CalledProcessError as e:
        print(f"Error running song.py: {e}")
        return f"Error running song.py: {e}", 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {e}", 500

    
@app.route('/lyrics3', methods=['POST'])
def lyrics3():
    paraphrased_file_path = "lyrics.html"
    if os.path.exists(paraphrased_file_path):
        return send_file(paraphrased_file_path, as_attachment=False)
    else:
        return "lyrics not", 502

@app.route('/map', methods=['POST'])
def map_file():
    paraphrased_file_path = "map.html"
    if os.path.exists(paraphrased_file_path):
        return send_file(paraphrased_file_path, as_attachment=False)
    else:
        return "Map file not found.", 503
    



def start_kara_process():
    try:
        response = requests.post("http://127.0.0.1:5002/kara")
        if response.status_code == 200:
            return send_file("song.html",as_attachment=False)
        else:
            return f"Failed to start kara process. Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error contacting kara service: {str(e)}"
    


@app.route('/kara', methods=['GET'])
def start_kara_route():
    # Call the /kara route in kara.py
    result = start_kara_process()
    return f"<p>{result}</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
