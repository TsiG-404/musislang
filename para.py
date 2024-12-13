import requests
from html import escape

# Function to read text from a file and process line by line
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# Function to split a line into chunks of 5 words
def split_into_chunks(line, chunk_size=15):
    #edo gia megethos protaseon 
    words = line.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to interact with LanguageTool API and get paraphrases for a chunk of text
def get_paraphrases(chunk):
    url = "https://api.languagetool.org/v2/check"
    data = {
        'text': chunk,
        'language': 'en',
    }
    response = requests.post(url, data=data)
    
    if response.status_code != 200:
        print(f"Error: Unable to connect to LanguageTool API. Status code: {response.status_code}")
        return []
    
    result = response.json()
    paraphrased_text = []
    
    # For each match (error or suggestion), extract the context and suggested correction
    for match in result.get('matches', []):
        context = match.get('context', {}).get('text', '')
        suggested_replacement = match.get('replacements', [])
        
        if suggested_replacement:
            paraphrased_text.append({
                'original': context,
                'suggestions': [replacement['value'] for replacement in suggested_replacement]
            })
    return paraphrased_text


def para2(chunk,lang):
    url = "https://api.languagetool.org/v2/check"
    data = {
        'text': chunk,
        'language': lang,
    }
    response = requests.post(url, data=data)
    
    if response.status_code != 200:
        print(f"Error: Unable to connect to LanguageTool API. Status code: {response.status_code}")
        return []
    
    result = response.json()
    paraphrased_text = []
    
    # For each match (error or suggestion), extract the context and suggested correction
    for match in result.get('matches', []):
        context = match.get('context', {}).get('text', '')
        suggested_replacement = match.get('replacements', [])
        
        if suggested_replacement:
            paraphrased_text.append({
                'original': context,
                'suggestions': [replacement['value'] for replacement in suggested_replacement]
            })
    return paraphrased_text

# Function to generate HTML content for paraphrased chunks
from html import escape

'''
def generate_html(paraphrased_texts):
    """Generate HTML content for the div dynamically."""
    content = ""
    for line_paraphrase in paraphrased_texts:
        content += f"<p><strong>Original:</strong> {escape(line_paraphrase['original'])}<br>"
        content += "<strong>Suggestions:</strong><ul>"
        for suggestion in line_paraphrase['suggestions']:
            content += f"<li>{escape(suggestion)}</li>"
        content += "</ul></p>"
    return content
'''
from bs4 import BeautifulSoup


def generate_html2(paraphrased_texts, html_template_path="paraphrased.html", placeholder_id="para"):
    """Generate HTML content dynamically and insert it into a specific div."""
    
    # Generate the dynamic HTML content
    content = ""
    for line_paraphrase in paraphrased_texts:
        content += f"<p><strong>Original:</strong> {escape(line_paraphrase['original'])}<br>"
        content += "<strong>Suggestions:</strong><ul>"
        for suggestion in line_paraphrase['suggestions']:
            content += f"<li>{escape(suggestion)}</li>"
        content += "</ul></p>"

    # Load the existing HTML file
    with open(html_template_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    # Find the placeholder div with the given ID
    placeholder_div = soup.find(id=placeholder_id)
    if not placeholder_div:
        # If the div doesn't exist, create it and append to the body
        placeholder_div = soup.new_tag("div", id=placeholder_id)
        soup.body.append(placeholder_div)

    # Insert the generated content into the placeholder div
    placeholder_div.clear()  # Clear any existing content in the div
    placeholder_div.append(BeautifulSoup(content, "html.parser"))

    # Save the updated HTML back to the file
    with open(html_template_path, "w", encoding="utf-8") as html_file:
        html_file.write(str(soup))

    print(f"Paraphrased text successfully added to the div '{placeholder_id}' in {html_template_path}")


def generate_html3(paraphrased_texts, html_template_path="paraphrased.html", placeholder_id="para2"):
    """Generate HTML content dynamically and insert it into a specific div."""
    
    # Generate the dynamic HTML content
    content = ""
    for line_paraphrase in paraphrased_texts:
        content += f"<p><strong>Original:</strong> {escape(line_paraphrase['original'])}<br>"
        content += "<strong>Suggestions:</strong><ul>"
        for suggestion in line_paraphrase['suggestions']:
            content += f"<li>{escape(suggestion)}</li>"
        content += "</ul></p>"

    # Load the existing HTML file
    with open(html_template_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    # Find the placeholder div with the given ID
    placeholder_div = soup.find(id=placeholder_id)
    if not placeholder_div:
        # If the div doesn't exist, create it and append to the body
        placeholder_div = soup.new_tag("div", id=placeholder_id)
        soup.body.append(placeholder_div)

    # Insert the generated content into the placeholder div
    placeholder_div.clear()  # Clear any existing content in the div
    placeholder_div.append(BeautifulSoup(content, "html.parser"))

    # Save the updated HTML back to the file
    with open(html_template_path, "w", encoding="utf-8") as html_file:
        html_file.write(str(soup))

    print(f"Paraphrased text successfully added to the div '{placeholder_id}' in {html_template_path}")


# Function to save the HTML content to a file
def save_html_to_file(html_content, output_file):
    with open(output_file, 'w') as file:
        file.write(html_content)



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

# Main function to process text file and generate HTML output
def main():
    #edo gia tin akliki verison
    input_file = "lyrics.txt"  # Text file to read from
    output_file = "paraphrased.html"  # HTML file to save results
    # Step 1: Read text from file line by line
    lines = read_text_file(input_file)

    # Step 2: Process each line and get paraphrases for each chunk of 5 words
    paraphrased_texts = []
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:  # Skip empty lines
            # Split the line into chunks of 5 words
            chunks = split_into_chunks(line)
            for chunk in chunks:
                paraphrases = get_paraphrases(chunk)
                if paraphrases:  # Only add paraphrased text if there are suggestions
                    for paraphrase in paraphrases:
                        paraphrase['original'] = chunk  # Add original chunk to the paraphrase entry
                    paraphrased_texts.extend(paraphrases)

    # Step 3: Generate HTML content
    #html_content = generate_html(paraphrased_texts)
    html_content =generate_html2(paraphrased_texts)

    # Step 4: Save the HTML content to a file
    #save_html_to_file(html_content, output_file)

    print(f"Paraphrased text saved to {output_file}")
    #edo telionei i agliki version

    #edo gia tin xeni glossa
    input_file = "translated.txt"  # Text file to read from
    output_file = "paraphrased.html"  # HTML file to save results
    # Step 1: Read text from file line by line
    lang=read_from_file("lang.txt")
    lines = read_text_file(input_file)

    # Step 2: Process each line and get paraphrases for each chunk of 5 words
    paraphrased_texts = []
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:  # Skip empty lines
            # Split the line into chunks of 5 words
            chunks = split_into_chunks(line)
            for chunk in chunks:
                paraphrases = para2(chunk,lang)
                if paraphrases:  # Only add paraphrased text if there are suggestions
                    for paraphrase in paraphrases:
                        paraphrase['original'] = chunk  # Add original chunk to the paraphrase entry
                    paraphrased_texts.extend(paraphrases)

    # Step 3: Generate HTML content
    #html_content = generate_html(paraphrased_texts)
    html_content =generate_html3(paraphrased_texts)

    # Step 4: Save the HTML content to a file
    #save_html_to_file(html_content, output_file)

    print(f"Paraphrased text saved to {output_file}")
    #edo telionei i agliki version


# Example usage
if __name__ == "__main__":
    
    main()
