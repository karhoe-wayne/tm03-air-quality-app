import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import api_usage  # Extract API Data

# Date Formatting Function for better visual
def formatted_date(date):
    day = date.day
    if 11 <= day <= 13:
        suffix = "th"  
    else :
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    formatted_date = date.strftime(f"%d{suffix} of %B, %Y")
    return formatted_date

# Setting all date formats and types
today = datetime.today().date()
today_str = today.isoformat()
formatted_today = formatted_date(today)

# Page Title
st.set_page_config(page_title="Air Quality Forecast for Malaysia", layout="wide")

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
        <h1>Air Quality Forecast for Malaysia</h1>
    </div>
""", unsafe_allow_html=True)

# Input Current Date
st.markdown(f"""
    <style>
        .custom-header {{
            font-size: 30px !important;  /* Adjust the font size */
        }}
    </style>
    <h2 class="custom-header">{formatted_today}</h2>
""", unsafe_allow_html=True)

# Display city selection box
col1, col2 = st.columns([1, 1])  # Creates two equal columns
with col1:  
    city = st.selectbox("Choose a city:", [""] + api_usage.obtain_formatted_cities_list())

if not city:  
    pass  # Do nothing
else:
    # Layout with two columns
    col1, col2 = st.columns([1, 1])
    with col1:
        # Extract values to be displayed
        o3 = next(item['avg'] for item in api_usage.obtain_data(city)['data']['forecast']['daily']['o3'] if item['day'] == today_str)
        pm25 = next(item['avg'] for item in api_usage.obtain_data(city)['data']['forecast']['daily']['pm25'] if item['day'] == today_str)
        pm10 = next(item['avg'] for item in api_usage.obtain_data(city)['data']['forecast']['daily']['pm10'] if item['day'] == today_str)
        uvi = next(item['avg'] for item in api_usage.obtain_data(city)['data']['forecast']['daily']['uvi'] if item['day'] == today_str)
        aqi = api_usage.obtain_data(city)['data']['aqi']
        
        # Color assignment for AQI box and map marker
        if aqi <= 50:
            aqi_color = '#70B31E'
            mark_color = 'green'
        elif 51 <= aqi <= 100: 
            aqi_color = '#FFDA00'
            mark_color = 'beige'
        elif 101 <= aqi <= 150:
            aqi_color = '#F78D1C'
            mark_color = 'orange'
        elif 151 <= aqi <= 200:
            aqi_color = '#C51A1A'
            mark_color = 'red'
        else:
            aqi_color = '#A020F0'
            mark_color = 'purple'
        
        # Display AQI Table
        st.markdown(f"""
            <style>
                .aqi-table {{
                    margin-top: 50px;
                    width: 80%;
                    border-collapse: collapse;
                    text-align: center;
                    font-size: 25px;
                    font-weight: bold;
                    background-color: #e0f3e0;
                    border-radius: 10px;
                }}
                .aqi-table th, .aqi-table td {{
                    padding: 25px;
                    border: 1px solid #ddd; 
                }}
                .aqi-box {{
                    background-color: {aqi_color};
                    padding: 25px;
                    border-radius: 10px;
                }}
            </style>
            <table class="aqi-table">
                <tr>
                    <td>O₃ <br> {o3}</td>
                    <td>PM₂.₅ <br> {pm25}</td>
                    <td>PM₁₀ <br> {pm10}</td>
                    <td>UVI <br> {uvi}</td>
                    <td class="aqi-box">AQI <br> {aqi}</td>
                </tr>   
            </table>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <p style="font-size: 14px; color: #555; margin-top: 20px;">
                <b> Each pollutant values are based on the AQI values that was obtained by <i>aqicn.org</i> based on their breakpoint tables. </b>
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <p style="font-size: 14px; color: #555;">
                <b> The displayed AQI represents the weekly air quality index. </b>
            </p>
            <hr>
        """, unsafe_allow_html=True)
        
        # Health Recommendations
        st.subheader("Health recommendations")
        st.markdown("""
            - 🟢 (API 0-50)    - A good day to be active outside!
            - 🟡 (API 51-100)  - Children should be aware and follow routine precautions
            - 🟠 (API 101-150) - Children should take precautions and manage existing conditions appropriately
            - 🔴 (API 150-200) - Children should avoid unnecessary outdoor activities if possible
            - 🟣 (API 201+)    - Children should avoid unnecessary outdoor activities at all cost
        """)
        
        st.markdown("""
            <p style="font-size: 14px; color: #555; margin-top: 8px;">
                <b> Health recommendations are suggested by <i>nyc.org</i> </b>
            </p>
            """, unsafe_allow_html=True)
    
    with col2:
        # Generate interactive Map
        m = folium.Map(location=[4.2105, 101.9758], zoom_start=7)
        
        # Add a marker with corresponding AQI caolor of selected city
        lat, long = api_usage.obtain_data(city)['data']['city']['geo']
        folium.Marker(
            location=[lat, long],
            icon=folium.Icon(color = mark_color, icon='none')
        ).add_to(m)
        
        # Display the map
        folium_static(m, width=800, height=700)

# Button to go to Trip Plan page
if st.button("Plan Your Trip"):
    st.switch_page("pages/plan_trip.py")
