import datetime
from geopy.distance import geodesic
import api_usage

# Obtain the forecast AQI values of different factors for a city on a specific date 
def get_aqi_values_for_city(city, date_str):
    data = api_usage.obtain_data(city)['data']['forecast']['daily']
    
    # Fetch max forecast AQI values for a city on a specific date.
    return max([
        next(item['avg'] for item in data[pollutant] if item['day'] == date_str)
        for pollutant in ['o3', 'pm25', 'pm10', 'uvi']
    ])

# Obtain the list of the trip route
def planned_trip(cities):
    # Ensure returns an empty list if no cities in the list
    if not cities:
        return []
    
    # Initialize time and travel route
    today = datetime.date.today()
    travel_plan = []
    
    # Create a copy of remaining cities to ensure all cities are covered
    remaining_cities = set(cities)
    
    # Start with the best AQI city for the 1st day
    current_date = today + datetime.timedelta(days = 1)
    # Get the AQI values for all cities
    city_aqi = {city: get_aqi_values_for_city(city, current_date.strftime("%Y-%m-%d")) for city in cities}
    
    # Choose the city with the lowest AQI as 1st destination
    start_city = min(city_aqi, key=city_aqi.get)  
    # Add to travel route list
    travel_plan.append(start_city)
    #Remove from list of remaining cities
    remaining_cities.remove(start_city)
    
    # Iterate the remaning cities
    while remaining_cities:
        # Instantiate and get the coordinates of previous city in the route
        prev_city = travel_plan[-1]
        prev_city_coord = tuple(api_usage.obtain_data(prev_city)['data']['city']['geo'])
        
        # Increment the date for the next city selection
        current_date += datetime.timedelta(days=1)
        # Get the AQI values for all remaining cities
        city_aqi = {city: get_aqi_values_for_city(city, current_date.strftime("%Y-%m-%d")) for city in remaining_cities}
        
        #Instantiate the next city to be added to the coute
        next_city = None
        
        ## Choose the next city to be added to the route
        # Sort the AQI values for the remaining cities
        for city in sorted(remaining_cities, key=lambda x: city_aqi[x]): 
            # Check if the distance between the previous city and the current city is less than 200 km
            city_coord = tuple(api_usage.obtain_data(city)['data']['city']['geo'])
            if geodesic(prev_city_coord, city_coord).km <= 200:
                # Found next city to be added
                next_city = city
                break
        
        # Add the next city to the route if distance criteria met
        if next_city:
            travel_plan.append(next_city)
            remaining_cities.remove(next_city)
        # If no city within 200 km, just pick the next best AQI city
        else:
            next_city = min(remaining_cities, key=lambda x: city_aqi[x])
            travel_plan.append(next_city)
            remaining_cities.remove(next_city)
    
    return travel_plan
