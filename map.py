import folium
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests

def get_coordinates(country_name):
    """
    Get the coordinates (latitude, longitude) of a country.
    """
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(country_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def create_map(country_name, artist_info):
    """
    Create a map centered on the country's coordinates, with artist information displayed below.
    """
    # Get the coordinates of the country
    latitude, longitude = get_coordinates(country_name)
    
    if latitude is None or longitude is None:
        print(f"Could not find the location for {country_name}")
        return
    
    # Create a map centered on the country's coordinates
    map_object = folium.Map(location=[latitude, longitude], zoom_start=3)
    
    # Add a marker for the country
    folium.Marker([latitude, longitude], popup=country_name).add_to(map_object)
    
    # Add artist information below the map
    html_info = f"""
    <div class="button-container">
<form action="/translate" method="POST">
<button type="submit">Translation</button>
</form>
<form action="/paraphrased" method="POST">
<button type="submit">grammar</button>
</form>
<form action="/lyrics3" method="POST">
<button type="submit">lyrics</button>
</form>
<form action="http://127.0.0.1:5002" method="GET">
<button type="submit">Karaoke</button>
</form>
</div>
    <div>
        <h2>Artist Information</h2>
        <p>{artist_info}</p>
    </div>
    
    """
    map_object.get_root().html.add_child(folium.Element(html_info))
    
    # Save the map as an HTML file
    map_object.save(f"map.html")
    print(f"Map for {country_name} with artist information saved as map.html")

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

def get_artist_info(artist_name):
    """
    Fetches detailed artist information from Wikipedia.
    """
    url = f"https://en.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Collect general description (intro paragraph)
        paragraphs = soup.find_all('p')
        description = None
        if paragraphs:
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                if text:
                    description = text
                    break

        # Extract additional info from infobox
        infobox = soup.find('table', {'class': 'infobox'})
        additional_info = {}
        if infobox:
            for row in infobox.find_all('tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    key = th.text.strip().lower()
                    value = td.text.strip()
                    additional_info[key] = value

        # Prepare a summary of the artist
        info_lines = [description or "No general description available."]
        for field in ['born', 'genres', 'occupation', 'instruments', 'years active']:
            if field in additional_info:
                info_lines.append(f"<strong>{field.capitalize()}:</strong> {additional_info[field]}")

        return "<br>".join(info_lines)
    except requests.RequestException as e:
        return f"Error fetching information for {artist_name}: {e}"

# Main logic
if __name__ == "__main__":
    country_file = "country.txt"  # The file containing the country name
    singer_file = "singer.txt"   # The file containing the artist name
    
    # Read country and artist names
    country_name = read_from_file(country_file)
    artist_name = read_from_file(singer_file)
    
    if country_name and artist_name:
        # Fetch artist information
        artist_info = get_artist_info(artist_name)
        
        # Create map with artist information
        create_map(country_name, artist_info)
    else:
        print("Country or artist name missing.")
