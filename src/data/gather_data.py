import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def collect_weather_data():
    api_key = os.getenv("VISUALCROSSING_API_KEY")
    city = "London"
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next5days"
    params = {
        "unitGroup": "metric",
        "key": api_key,
        "contentType": "json"
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()

    weather_data = []
    for day in data["days"][:5]:  # limit to 5 days
        weather_data.append({
            "date_time": datetime.strptime(day["datetime"], "%Y-%m-%d"),
            "temperature": day["temp"],
            "humidity": day["humidity"],
            "wind_speed": day["windspeed"],
            "weather_condition": day["conditions"]
        })

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(weather_data)
    df.to_csv("data/raw_data.csv", index=False)

if __name__ == "__main__":
    collect_weather_data()