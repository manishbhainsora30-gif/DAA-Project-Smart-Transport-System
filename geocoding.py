from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="smart_transport")

def get_coordinates(place):
    loc = geolocator.geocode(place)
    if loc:
        return (loc.latitude, loc.longitude)
    return None