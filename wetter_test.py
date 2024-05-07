import tkinter as tk
import requests

API_KEY = "2161b62970176f7d1fe6d003694cb8b5"
CITY = "Bocholt"
COUNTRY_CODE = "DE"
LANGUAGE = "de"
UNIT = "metric"


def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={API_KEY}&units={UNIT}&lang={LANGUAGE}"
        response = requests.get(url)
        weather_data = response.json()

        city_label.config(text=weather_data['name'])
        temperature_label.config(text=f"Temperatur: {weather_data['main']['temp']}°C")
        humidity_label.config(text=f"Feuchtigkeit: {weather_data['main']['humidity']}%")
        description_label.config(text=f"Wetter: {weather_data['weather'][0]['description'].capitalize()}")
    except:
        print("Etwas ist schief gelaufen")



# GUI Setup
root = tk.Tk()
root.title("Wetter App")
root.geometry("400x500")

city_label = tk.Label(root, font=('Helvetica', 20))
city_label.pack()

temperature_label = tk.Label(root, font=('Helvetica', 16))
temperature_label.pack()

humidity_label = tk.Label(root, font=('Helvetica', 16))
humidity_label.pack()

description_label = tk.Label(root, font=('Helvetica', 16))
description_label.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack()

root.mainloop()
