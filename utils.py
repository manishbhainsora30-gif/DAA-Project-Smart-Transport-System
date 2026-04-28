import folium

def create_map(location):
    return folium.Map(location=location, zoom_start=13)

def add_markers(m, start, end, src, dst):
    folium.Marker(
        start,
        popup=src,
        tooltip=src,
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Marker(
        end,
        popup=dst,
        tooltip=dst,
        icon=folium.Icon(color="red")
    ).add_to(m)

    return m

def add_routes_to_map(m, routes, selected_index=0):
    colors = ["blue", "gray", "black"]

    for idx, route in enumerate(routes):
        coords = route["coords"]

        if idx == selected_index:
            color = "red"
            weight = 8
            opacity = 1
        else:
            color = colors[idx % len(colors)]
            weight = 4
            opacity = 0.5

        folium.PolyLine(
            coords,
            color=color,
            weight=weight,
            opacity=opacity,
            tooltip=f"Route {idx+1} ({route['traffic']})"
        ).add_to(m)

    return m


# ✅ FIXED: Hospital names always visible
def add_hospitals(m, hospitals):
    for name, lat, lon in hospitals:

        # Main marker
        folium.Marker(
            [lat, lon],
            popup=f"<b>🏥 {name}</b>",
            tooltip=name,
            icon=folium.Icon(color="blue", icon="plus-sign")
        ).add_to(m)

        # Permanent text label
        folium.map.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 12px;
                    color: blue;
                    font-weight: bold;
                ">
                    🏥 {name}
                </div>
                """
            )
        ).add_to(m)

    return m