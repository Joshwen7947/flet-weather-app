import flet as ft
import requests
from keys import API_KEY

# Remember to import your own API key!
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
MAP_URL = "https://www.openstreetmap.org/export/embed.html?bbox={lon}%2C{lat}%2C{lon}%2C{lat}&layer=mapnik"

# Function to fetch data from OpenWeather API
def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
        }
    return None


# Main function to build the Flet app
def main(page: ft.Page):
    page.title = "Weather App"
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.padding = 20 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 700 
    
    # Input field for city name
    city_input = ft.TextField(
        label="Enter City",
        width=300,
        bgcolor=ft.colors.WHITE,
        color=ft.colors.BLACK,
        border_radius=10,
    )
    
    # Text element to display the weather results
    result_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    
    # WebView to display the map (hidden initially)
    map_frame = ft.WebView(url="", width=600, height=400, visible=False)
    
    # Function to handle the search button click
    def search_weather(e):
        city = city_input.value.strip() 
        if not city:
            result_text.value = "Please enter a city name."
            page.update()
            return
        
        weather_data = get_weather(city)  # Fetch weather data from API
        
        if weather_data:
            # Update text with weather details
            result_text.value = f"City: {weather_data['city']}\nTemperature: {weather_data['temp']}°C\nHumidity: {weather_data['humidity']}%\nWeather: {weather_data['weather']}"
            
            # Update the map URL and make it visible
            map_frame.url = MAP_URL.format(lat=weather_data['lat'], lon=weather_data['lon'])
            map_frame.visible = True
        else:
            result_text.value = "City not found. Please try again."
            map_frame.visible = False
        
        page.update()  # Refresh the UI
    
    # Search button to trigger the weather search
    search_button = ft.ElevatedButton(
        "Search",
        on_click=search_weather,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=10)
    )
    
    # Container to hold UI elements and align them
    container = ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Weather App", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                city_input,
                search_button,
                result_text,
                map_frame,
            ],
        ),
        alignment=ft.alignment.center,
        padding=20,
        border_radius=15,
        bgcolor=ft.colors.BLUE_GREY_800,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.BLACK12)
    )
    
    # Add container to the page
    page.add(container)

# Run the Flet app
if __name__ == "__main__":
    ft.app(target=main)