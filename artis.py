import requests
from bs4 import BeautifulSoup

# Define the user-agent string
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

def get_artist_country(artist_name):
    """
    Fetches the country of birth of an artist from their Wikipedia page.

    :param artist_name: The name of the artist (string)
    :return: Country or a message if not found
    """
    # Create the Wikipedia URL for the artist's page
    url = f"https://en.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"
    
    # Set the user-agent for the request
    headers = {'User-Agent': user_agent}

    try:
        # Send GET request to Wikipedia
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for invalid status codes (e.g., 404)
        
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for the nationality in the infobox (where it's usually located)
        infobox = soup.find('table', {'class': 'infobox'})

        if not infobox:
            return f"Sorry, the infobox for '{artist_name}' could not be found."

        # Look through the infobox rows to find the "Born" field
        for row in infobox.find_all('tr'):
            th = row.find('th')
            td = row.find('td')
            if th and td and 'born' in th.text.lower():
                born_text = td.text.strip()

                # Extract country (last part of the location, typically after the last comma)
                parts = born_text.split(',')
                country = parts[-1].strip() if len(parts) > 1 else "Unknown"

                # Save the country to the file
                with open("country.txt", 'w') as file1:
                    file1.write(country)

                return f"Country saved: {country}"

        return f"Could not find country information for '{artist_name}'."
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"

def read_artist_name_from_file(file_path):
    """
    Reads the artist's name from a text file.

    :param file_path: Path to the text file containing the artist's name
    :return: The artist's name as a string
    """
    try:
        with open(file_path, 'r') as file:
            artist_name = file.readline().strip()  # Read the first line and strip whitespace
            return artist_name
    except FileNotFoundError:
        return None

# Example usage
if __name__ == "__main__":
    artist_file = "singer.txt"  # Text file containing the artist's name
    artist_name = read_artist_name_from_file(artist_file)
    
    if artist_name:
        result = get_artist_country(artist_name)
        print(result)
    else:
        print(f"Error: The file '{artist_file}' does not exist or is empty.")
