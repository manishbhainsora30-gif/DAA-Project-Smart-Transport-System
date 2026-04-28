import requests

# -------------------------------
# FALLBACK HOSPITALS (DEHRADUN)
# -------------------------------
FALLBACK_HOSPITALS = [
    ("Doon Hospital", 30.3256, 78.0437),
    ("Velmed Hospital", 30.3168, 78.0402),
    ("Synergy Institute of Medical Sciences", 30.3505, 78.0550),
    ("Max Super Speciality Hospital", 30.3512, 78.0635),
    ("Graphic Era Hospital", 30.2682, 78.0440),
]

# -------------------------------
# GET HOSPITALS
# -------------------------------
def get_nearby_hospitals(lat, lon, radius=8000):
    url = "http://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      relation["amenity"="hospital"](around:{radius},{lat},{lon});
    );
    out center;
    """

    try:
        res = requests.get(url, params={"data": query}, timeout=5)
        data = res.json()

        hospitals = []

        for el in data.get("elements", []):
            name = el.get("tags", {}).get("name", "Hospital")

            lat_val = el.get("lat") or el.get("center", {}).get("lat")
            lon_val = el.get("lon") or el.get("center", {}).get("lon")

            if lat_val and lon_val:
                hospitals.append((name, lat_val, lon_val))

        # ✅ If API fails → use fallback
        if not hospitals:
            return FALLBACK_HOSPITALS

        return hospitals[:5]

    except:
        # ✅ API completely failed
        return FALLBACK_HOSPITALS


# -------------------------------
# NEAREST HOSPITAL
# -------------------------------
def nearest_hospital(user_location):
    hospitals = get_nearby_hospitals(user_location[0], user_location[1])

    def dist(h):
        return (h[1] - user_location[0])**2 + (h[2] - user_location[1])**2

    return min(hospitals, key=dist)