import streamlit as st
from streamlit_folium import st_folium


from routing import get_routes, extract_routes
from hospital import nearest_hospital, get_nearby_hospitals
from utils import create_map, add_routes_to_map, add_markers, add_hospitals
from geocoding import get_coordinates
from config import DEFAULT_LOCATION

st.set_page_config(layout="wide")
st.title("🚗 Smart Transport System")

# ---------------- SESSION ----------------
if "map" not in st.session_state:
    st.session_state.map = create_map(DEFAULT_LOCATION)

if "routes" not in st.session_state:
    st.session_state.routes = None

if "selected_route" not in st.session_state:
    st.session_state.selected_route = 0

# ---------------- INPUT ----------------
src = st.text_input("Source", "ISBT Dehradun")
dst = st.text_input("Destination", "Clock Tower Dehradun")

col1, col2 = st.columns(2)
get_route_btn = col1.button("Get Routes")
emergency_btn = col2.button("🚑 Emergency Route")

# ---------------- ROUTE SELECTION ----------------
if st.session_state.routes:
    st.session_state.selected_route = st.radio(
        "Select Route",
        options=list(range(len(st.session_state.routes))),
        format_func=lambda x: f"Route {x+1}",
        index=st.session_state.selected_route
    )

# ---------------- GET ROUTES ----------------
if get_route_btn:
    start = get_coordinates(src)
    end = get_coordinates(dst)

    if not start or not end:
        st.error("Invalid location")
    else:
        m = create_map(start)

        hospitals = get_nearby_hospitals(start[0], start[1])
        m = add_hospitals(m, hospitals)

        m = add_markers(m, start, end, src, dst)

        data = get_routes(start, end)

        if data:
            routes = extract_routes(data)

            if routes:
                st.session_state.routes = routes

                best_index = min(
                    range(len(routes)),
                    key=lambda i: routes[i]["duration"]
                )
                st.session_state.selected_route = best_index

                m = add_routes_to_map(m, routes, best_index)

        st.session_state.map = m

# ---------------- EMERGENCY ROUTE ----------------
if emergency_btn:
    start = get_coordinates(src)

    if not start:
        st.error("Invalid source location")
    else:
        hospital = nearest_hospital(start)
        hospitals = get_nearby_hospitals(start[0], start[1])

        if hospital:
            name, lat, lon = hospital

            m = create_map(start)
            m = add_hospitals(m, hospitals)
            m = add_markers(m, start, (lat, lon), src, name)

            data = get_routes(start, (lat, lon))

            if data:
                routes = extract_routes(data)
                if routes:
                    st.session_state.routes = routes[:1]
                    st.session_state.selected_route = 0
                    m = add_routes_to_map(m, routes[:1], 0)

            st.session_state.map = m
            st.success(f"🚑 Routing to nearest hospital: {name}")
        else:
            st.warning("⚠️ No hospital found via API, try again")

# ---------------- UPDATE MAP ----------------
if st.session_state.routes:
    start = get_coordinates(src)
    end = get_coordinates(dst)

    if start and end:
        m = create_map(start)
        m = add_markers(m, start, end, src, dst)
        m = add_routes_to_map(
            m,
            st.session_state.routes,
            st.session_state.selected_route
        )
        st.session_state.map = m

# ---------------- SHOW MAP ----------------
st_folium(
    st.session_state.map,
    width=1200,
    height=500
)

# ---------------- ROUTE INFO ----------------
if st.session_state.routes:
    for i, r in enumerate(st.session_state.routes):
        if i == st.session_state.selected_route:
            st.success(
                f"✅ Route {i+1}: {r['distance']:.2f} km | "
                f"{r['duration']:.2f} min | 🚦 {r['traffic']} (SELECTED)"
            )
        else:
            st.write(
                f"Route {i+1}: {r['distance']:.2f} km | "
                f"{r['duration']:.2f} min | 🚦 {r['traffic']}"
            )