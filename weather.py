from dotenv import load_dotenv
from pprint import pprint
import requests
import os
from datetime import datetime

load_dotenv()

def get_five_day_forecast(location="Lexington"):
    api_key = os.getenv("API_KEY")
    request_url = f'http://api.openweathermap.org/data/2.5/forecast?appid={api_key}&q={location}&units=imperial'
    
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        forecast_data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"cod": "error", "message": str(e)}
    
    return forecast_data
def get_weather_by_coords(lat, lon):
    request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&lat={lat}&lon={lon}&units=imperial'
    weather_data = requests.get(request_url).json()
    return weather_data

def parse_forecast_data(forecast_data):
    daily_forecast = {}
    for entry in forecast_data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        temp = entry["main"]["temp"]
        description = entry["weather"][0]["description"]
        
        if date not in daily_forecast:
            daily_forecast[date] = {
                "temps": [],
                "descriptions": []
            }
        
        daily_forecast[date]["temps"].append(temp)
        daily_forecast[date]["descriptions"].append(description)
    
    summary_forecast = []
    for date, data in daily_forecast.items():
        avg_temp = sum(data["temps"]) / len(data["temps"])
        most_common_description = max(set(data["descriptions"]), key=data["descriptions"].count)
        summary_forecast.append({
            "date": datetime.strptime(date, "%Y-%m-%d").strftime("%A, %B %d"),
            "avg_temp": f"{avg_temp:.1f}",
            "description": most_common_description.capitalize()
        })
    
    return summary_forecast

if __name__ == "__main__":
    print('\n*** Get 5-Day Weather Forecast ***\n')
    
    city = input("\nPlease enter a city name: ").strip()
    state = input("\nPlease enter a state name (optional): ").strip()
    
    location = f"{city},{state}" if state else city
    
    if not location.strip():
        location = "Lexington"
    
    forecast_data = get_five_day_forecast(location)
    
    if 'cod' in forecast_data and forecast_data['cod'] == "200":
        summary_forecast = parse_forecast_data(forecast_data)
        print("\n")
        pprint(summary_forecast)
    else:
        print("Error fetching forecast data")
