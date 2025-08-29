# utils/agriculture_api.py
import requests
from datetime import date, timedelta

def get_agriculture_data(lat, lon):
    """
    Returns agriculture insights given latitude and longitude:
    - temperature_avg: average temperature last 7 days
    - precipitation_total: total rainfall last 7 days
    - suggested_crops: list of suggested crops based on climate
    """
    try:
        today = date.today()
        start = today - timedelta(days=6)  # last 7 days
        start_str = start.strftime("%Y%m%d")
        end_str = today.strftime("%Y%m%d")

        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters=T2M,PRECTOTCORR&community=AG&longitude={lon}&latitude={lat}"
            f"&start={start_str}&end={end_str}&format=JSON"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        parameters = data.get("properties", {}).get("parameter", {})
        temperatures = parameters.get("T2M", {})
        rainfall = parameters.get("PRECTOTCORR", {})

        # Filter out missing data (-999.0)
        temp_values = [v for v in list(temperatures.values()) if v != -999.0][-7:]
        rain_values = [v for v in list(rainfall.values()) if v != -999.0][-7:]

        temperature_avg = round(sum(temp_values)/len(temp_values), 1) if temp_values else "N/A"
        precipitation_total = round(sum(rain_values), 1) if rain_values else "N/A"

        # Suggested crops based on simple rules
        suggested_crops = []
        if temperature_avg != "N/A" and precipitation_total != "N/A":
            if temperature_avg > 25 and precipitation_total > 50:
                suggested_crops = ["Maize", "Rice"]
            elif temperature_avg > 20:
                suggested_crops = ["Beans", "Tomatoes"]
            else:
                suggested_crops = ["Wheat", "Barley"]

        return {
            "temperature_avg": temperature_avg,
            "precipitation_total": precipitation_total,
            "suggested_crops": suggested_crops
        }

    except Exception:
        return {
            "temperature_avg": "N/A",
            "precipitation_total": "N/A",
            "suggested_crops": []
        }
