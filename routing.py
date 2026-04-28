import requests
import polyline
import random


# -------------------------------
# GET SINGLE ROUTE FROM OSRM
# -------------------------------
def get_single_route(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}"
    
    params = {
        "overview": "full",
        "geometries": "polyline"
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        if "routes" in data:
            return data["routes"][0]

    except:
        return None

    return None



def merge_polylines(poly1, poly2):
    coords1 = polyline.decode(poly1)
    coords2 = polyline.decode(poly2)

    # merge properly
    merged_coords = coords1 + coords2

    return polyline.encode(merged_coords)


# -------------------------------
# GENERATE 3 DIFFERENT ROUTES
# -------------------------------
def get_routes(start, end):
    routes = []

    # Route 1 → direct
    r1 = get_single_route(start, end)
    if r1:
        routes.append(r1)

    # Route 2 & 3 → via midpoints
    for offset in [0.01, 0.02]:
        mid = (
            (start[0] + end[0]) / 2 + random.uniform(-offset, offset),
            (start[1] + end[1]) / 2 + random.uniform(-offset, offset)
        )

        rA = get_single_route(start, mid)
        rB = get_single_route(mid, end)

        if rA and rB:
            merged_geometry = merge_polylines(
                rA["geometry"],
                rB["geometry"]
            )

            routes.append({
                "geometry": merged_geometry,  # ✅ FIXED
                "distance": rA["distance"] + rB["distance"],
                "duration": rA["duration"] + rB["duration"]
            })

    return {"routes": routes}


# -------------------------------
# EXTRACT ROUTES + TRAFFIC
# -------------------------------
def extract_routes(data):
    if not data or "routes" not in data:
        return []

    routes = []

    for route in data["routes"]:
        coords = polyline.decode(route["geometry"])
        distance = route["distance"] / 1000
        duration = route["duration"] / 60

        # traffic estimation
        if duration < 10:
            traffic = "Low"
        elif duration < 18:
            traffic = "Medium"
        else:
            traffic = "High"

        routes.append({
            "coords": coords,
            "distance": distance,
            "duration": duration,
            "traffic": traffic
        })

    return routes