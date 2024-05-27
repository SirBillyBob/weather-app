from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from weather import get_five_day_forecast, get_weather_by_coords, parse_forecast_data
from waitress import serve
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

@app.route('/')
@app.route('/index')
def index():
    recent_searches = session.get('recent_searches', [])
    return render_template('index.html', recent_searches=recent_searches)

@app.route('/weather')
def get_weather():
    city = request.args.get('city', '').strip()
    state = request.args.get('state', '').strip()
    
    if not city:
        city = "Lexington"
    
    location = f"{city},{state}" if state else city
    
    forecast_data = get_five_day_forecast(location)
    
    if 'cod' not in forecast_data or forecast_data['cod'] != "200":
        return render_template('not-found.html'), 404
    
    recent_searches = session.get('recent_searches', [])
    if location not in recent_searches:
        recent_searches.insert(0, location)
        if len(recent_searches) > 5:
            recent_searches.pop()
        session['recent_searches'] = recent_searches
    
    summary_forecast = parse_forecast_data(forecast_data)
    
    return render_template(
        "weather.html",
        title=f"5-Day Forecast for {forecast_data['city']['name']}",
        forecast=summary_forecast
    )

@app.route('/get_weather_by_coords')
def get_weather_by_coords_route():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    weather_data = get_weather_by_coords(lat, lon)
    return jsonify(weather_data)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('recent_searches', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
