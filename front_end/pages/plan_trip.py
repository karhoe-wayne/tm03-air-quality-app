import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime
import api_usage  # Extract API Data
import route_planner  # Route Planning functions

# Page Title
st.set_page_config(page_title="Find Your Cleanest Path: Real-Time Air Quality Routes", layout="wide")

# Custom CSS for title and background
st.markdown("""
    <style>
        body, .stApp {
            background-color: #d4edda !important;
        }
        .title {
            display: flex;
            align-items: center;
            padding: 10px;
            width: 100%;
        }               
        .title h1 {
            margin: 0;
            font-size: 60px;
            font-weight: normal !important;
            color: green;
            font-family: Arial, sans-serif;
        }
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
            display: none !important;
        }
        h1 a, [data-testid="stSidebar"], [data-testid="stSidebarNav"], 
        [data-testid="collapsedControl"] { 
            display: none !important; 
        }
    </style>
    <div class='title'>
        <h1>Find Your Cleanest Path: Real-Time Air Quality Routes</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="font-size: 20px; color: #555; margin-top: 8px;">
        <b> Let Us Plan Your Adventure For The Next 2-5 days! (A different city everyday) </b>
    </p>
""", unsafe_allow_html=True)

# Custom CSS for selected option box
st.markdown("""
    <style>
        span[data-baseweb="tag"] {
            background-color: #e0f3e0 !important;  
            color: black !important;  
            border-radius: 5px !important;  
        }
    </style>
""", unsafe_allow_html=True)

# Create selection box for cities
city_options = api_usage.obtain_formatted_cities_list()
selected_cities = st.multiselect("Choose the cities you would like to visit: (up to FIVE cities)", city_options)

# Restrict city selections to a minimum of 2 and maximum of 5
if len(selected_cities) <= 0:
    pass
elif len(selected_cities) == 1:
    st.warning("⚠️ Please select more than one city.") 
elif len(selected_cities) > 5:
    st.warning("⚠️ You can only select up to 5 options. Please remove some selections.") 
else :
    # Generate the list of cities in order of the route
    city_route = route_planner.planned_trip(selected_cities)
    
    col1, col2 = st.columns([1, 1]) 
    with col1:
        # Display suggested route on the map 
        line_coords = []
        for city in city_route:
            city_coord = api_usage.obtain_data(city)['data']['city']['geo']
            line_coords.append(city_coord)
        
        # Generate interactive Map
        m = folium.Map(location=[4.2105, 101.9758], zoom_start=7)
        
        # Draw the routes according to the routes obtained
        folium.PolyLine(
            line_coords,
            color="red",
            weight=5,
            opacity=0.8
        ).add_to(m)
        
        # Add a marker to show the 1st city in the route
        lat_start, long_start = line_coords[0]
        folium.Marker(
            location=[lat_start, long_start],
            icon=folium.Icon(color = 'red', icon='none')
        ).add_to(m)
        
        # Display the map
        folium_static(m, width=800, height=700)
    
    with col2:
        # Display table for days and cities based on the route
        table_rows = ""
        for day_no, city in enumerate(city_route, start=1):
            table_rows += f"<tr><td>Day-{day_no}</td><td>{city}</td></tr>"
        
        st.markdown(f"""
            <style>
            table {{
                margin-top: 155px;
                margin-left: 50px;
                width: 70%;
                border-collapse: collapse;
                border: 2px solid black; 
                text-align: center;
                font-size: 20px;
                background-color: #e0f3e0; 
            }}
            th, td {{
                border: 1px solid black !important; 
                padding: 20px;
            }}
            th {{
                background-color: lightgray;
            }}
            </style>
            <table>
                <tr>
                    <th>Days</th>
                    <th>Cities to Visit</th>
                </tr>
                {table_rows}
            </table>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <p style="font-size: 14px; color: #555; margin-top: 8px; margin-left: 50px;">
                <b> Routes are suggested based on daily AQI values. </b>
            </p>
        """, unsafe_allow_html=True)

# Button to go to Daily Forecast page
if st.button("Back to Daily Forecast"):
    st.switch_page("forecast.py")

