import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

def get_weather(city):
    """
    Fetch weather data for a city from OpenWeatherMap.
    Returns a dictionary with temperature, humidity, wind speed, condition, and icon URL.
    Handles errors gracefully and provides default values.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # HTTP errors will raise exceptions
        data = r.json()

        return {
            "temperature": data.get("main", {}).get("temp", "N/A"),
            "humidity": data.get("main", {}).get("humidity", "N/A"),
            "wind_speed": data.get("wind", {}).get("speed", "N/A"),
            "condition": data.get("weather", [{}])[0].get("description", "N/A"),
            "icon_url": f"http://openweathermap.org/img/wn/{data.get('weather',[{}])[0].get('icon','')}@2x.png"
        }
        
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    except ValueError as e:
        print("Failed to decode JSON:", e)
    
    # Default response if anything goes wrong
    return {
        "temperature": "N/A",
        "humidity": "N/A",
        "wind_speed": "N/A",
        "condition": "N/A",
        "icon_url": ""
    }
