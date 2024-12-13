import os
from bs4 import BeautifulSoup
import os
from googletrans import Translator
#from googletrans_new import Translator


def translate_file(input_file, target_language, txt_output_file, html_output_file):
    """
    Translate the content of a text file to a specified language and save it to both a .txt and .html file.

    :param input_file: Path to the input .txt file containing the text to translate
    :param target_language: Target language code (e.g., 'es' for Spanish, 'fr' for French)
    :param txt_output_file: Path to save the translated .txt file
    :param html_output_file: Path to save the translated .html file
    """
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    try:
        # Initialize the translator
        translator = Translator()

        # Read the input file
        with open(input_file, "r", encoding="utf-8") as file:
            text_to_translate = file.read()

        # Translate the text
        print(f"Translating to '{target_language}'...")
        translated = translator.translate(text_to_translate, dest=target_language)

        # Save the translated text to the output .txt file
        with open(txt_output_file, "w", encoding="utf-8") as txt_file:
            txt_file.write(translated.text)
        print(f"Translated text saved to '{txt_output_file}'")

        # Replace newlines with <br> for the HTML file
        html_translated_text = translated.text.replace("\n", "<br>")

        # Save the translated text to an HTML file within a <div> with class 'translate'
        html_content = f"""
        <html>
        <head>
            <title>Translation</title>
        </head>
        <body>
            <h1>Translated Text</h1>
            <div class='translate'>{html_translated_text}</div>
        </body>
        </html>
        """
        with open(html_output_file, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        print(f"Translated text saved to HTML file: '{html_output_file}'")
    except Exception as e:
        print(f"An error occurred during translation: {e}")



def save_lyrics_to_files(translation_text="translated.txt", html_template_path="lyrics.html", placeholder_id="translate", translation_id="translate"):
    """
    Save lyrics, song title, and translated text to a plain text file and update a specific part of an HTML file.

    - lyrics_text: Plain text of the lyrics.
    - lyrics_html: HTML-formatted lyrics.
    - song_title: Title of the song.
    - translation_text: Translated text of the lyrics (optional).
    - html_template_path: Path to the existing HTML file to update.
    - placeholder_id: ID of the <div> to update with the original lyrics.
    - translation_id: ID of the <div> to update with the translated text.
    """
    txt_file_path = "translated.txt"

    

    try:
        # Check if the template HTML file exists
        if not os.path.exists(html_template_path):
            print(f"HTML template '{html_template_path}' not found. Creating a new one.")
            with open(html_template_path, "w", encoding="utf-8") as new_html_file:
                # Create a basic HTML template with placeholders
                new_html_file.write(
                    f"<html><body><h1 id='song2'></h1>\n"
                    f"<div id='{placeholder_id}'></div>\n"
                    f"<div id='{translation_id}'></div></body></html>"
                )

        # Load the existing HTML file
        with open(html_template_path, "r", encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")

        '''
        # Update the song title
        title_placeholder = soup.find(id="song2")
        if not title_placeholder:
            title_placeholder = soup.new_tag("h1", id="song2")
            soup.body.insert(0, title_placeholder)
        title_placeholder.string = song_title  # Set the title text
        '''
        # Find the placeholder div for original lyrics by ID
        placeholder = soup.find(id=placeholder_id)
        if not placeholder:
            print(f"Error: No element with ID '{placeholder_id}' found.")
            return

        

        # Find the placeholder div for translation by ID
        translation_placeholder = soup.find(id=translation_id)
        if not translation_placeholder:
            print(f"Error: No element with ID '{translation_id}' found. Adding one.")
            translation_placeholder = soup.new_tag("div", id=translation_id)
            soup.body.append(translation_placeholder)

        # Replace the content of the translation placeholder with the translated text
        if translation_text:
            translation_placeholder.clear()
            translation_placeholder.string = translation_text

        # Save the updated HTML back to the file
        with open(html_template_path, "w", encoding="utf-8") as html_file:
            html_file.write(str(soup))
        print(f"Lyrics and translation successfully saved to {html_template_path}")
    except Exception as e:
        print(f"Error updating HTML file: {str(e)}")

# Example usage


#edoooo!!!!
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



def read_from_file(file_path):
    """
    Reads the first line of a text file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip()  # Read the first line and strip whitespace
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    


def main():
    input_file = "lyrics.txt"  # Replace with your input file path

    target_language =read_from_file("lang.txt")  # Replace with your target language code (e.g., 'es' for Spanish)

    txt_output_file = "translated.txt"  # Path for the translated .txt file
    html_output_file = "translated.html"  # Path for the translated .html file

    translate_file(input_file, target_language, txt_output_file, html_output_file)

    #edo!!!!
    traslate(
        lyrics_text="translated.txt",
        html_template_path="lyrics.html",
        placeholder_id="translate"
        
    )
    

if __name__ == "__main__":
    main()
