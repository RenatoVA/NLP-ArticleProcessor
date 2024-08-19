import requests

def search_city(city_name, username, max_rows=10):
    base_url = "http://api.geonames.org/searchJSON"
    params = {
        'q': city_name,
        'maxRows': max_rows,
        'username': username
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_country_and_continent(city_name, username):
    results = search_city(city_name, username)
    if results and 'geonames' in results and len(results['geonames']) > 0:
        place = results['geonames'][0]
        country = place.get('countryName')
        continent_code = place.get('continentCode')
        continent = continent_name(continent_code) if continent_code else "N/A"
        return {
            'city': place.get('name'),
            'country': country,
            'continent': continent
        }
    else:
        return None

def continent_name(continent_code):
    continents = {
        "AF": "Africa",
        "AS": "Asia",
        "EU": "Europe",
        "NA": "North America",
        "OC": "Oceania",
        "SA": "South America",
        "AN": "Antarctica"
    }
    return continents.get(continent_code, "Unknown")

# Ejemplo de uso
username = "remii3322"  # Reemplaza con tu nombre de usuario de GeoNames
city_name = "London"
info = get_country_and_continent(city_name, username)

if info:
    print(f"Ciudad: {info['city']}, País: {info['country']}, Continente: {info['continent']}")
else:
    print("No se encontró información sobre la ciudad.")