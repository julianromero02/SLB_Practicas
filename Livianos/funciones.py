
from geopy.geocoders import Nominatim

from geopy.distance import geodesic 
import requests

def geocode_location(geolocator, location):
    try:
        return geolocator.geocode(f"{location}, COLOMBIA")
    except Exception as e:
        return None

def distanciaReal(inicio, fin):
    geolocator = Nominatim(user_agent="my-app")

    # Mapping for custom location names
    location_mapping = {
        "ACACIAS":"Acacías, Piedemonte, Meta",
        "CASTILLA": "CASTILLA LA NUEVA,META",
        "RUBIALES": "PUERTO GAITAN,META",
        "PUERTO GAITAN": "PUERTO GAITAN,META",
        "OASIS": "OASIS,META",
        "CHIPAQUE": "CHIPAQUE,CUNDINAMARCA",
        'PENDARE':"PENDARE,PUERTO GAITAN",
        "BUCARAMANGA":"Aeropuerto Internacional Palonegro",
        "YOPAL":"YOPAL,CASANARE",
        "VILLANUEVA":"VILLANUEVA,CASANARE",
        "VALLEDUPAR":"VALLEDUPAR, CESAR",
        "AGUACHICA":"AGUACHICA, CESAR",
        "RUBIALES":"Campo Rubiales, Puerto Gaitán",
        "CRISTALINA":"La Cristalina, Puerto Gaitán, Rio Meta",
        "CHICHIMENE":"Chichimene, San Carlos de Guaroa, Piedemonte, Meta, RAP (Especial) Central, Colombia"
    }

    # Convert custom location names to actual names
    inicio = location_mapping.get(inicio, inicio)
    fin = location_mapping.get(fin, fin)

    Origen = geocode_location(geolocator, inicio)
    Destino = geocode_location(geolocator, fin)

    # Check if geocoding failed for either origin or destination
    if Origen is None:
        return 100
        return f"No se pudo encontrar la ubicación para '{inicio}'"
    if Destino is None:
        return 100
        return f"No se pudo encontrar la ubicación para '{fin}'"

    # Check if longitude and latitude attributes exist for Origen and Destino
    if hasattr(Origen, 'longitude') and hasattr(Origen, 'latitude') and hasattr(Destino, 'longitude') and hasattr(Destino, 'latitude'):
        url = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}?overview=false"
        url = url.format(Origen.longitude, Origen.latitude, Destino.longitude, Destino.latitude)

        try:
            response = requests.get(url)
            data = response.json()

            if "routes" in data and len(data["routes"]) > 0:
                distancia = data["routes"][0]["distance"] / 1000
                return distancia
            else:
                distancia = 100 # Asignar un valor predeterminado aquí   distancia = "No se pudo calcular la distancia"
                return distancia

        except requests.exceptions.RequestException as e:
            distancia = f"Error de conexión: {str(e)}"  # Asignar un valor predeterminado aquí
            return distancia
    else:
        return "Error: No se encontraron coordenadas para calcular la distancia"

# Rest of your code remains unchanged...
