import requests
import customtkinter
from PIL import Image
import os

# Set dark theme to match the mockup
customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.geometry("800x600")
app.title("Weather App")

API_KEY = "592826e13ba208386547ce38c45167e9"
recent_searches_list = []

# --- Helper Function for Icons ---
def get_weather_icon(weather_id, icon_code):
    """Maps OpenWeatherMap API IDs to your local Assets folder images."""
    icon_file = "6p.png"  # Default fallback (cloud)
    
    if 200 <= weather_id <= 232: 
        icon_file = "1p.png" # Thunderstorm
    elif 300 <= weather_id <= 321: 
        icon_file = "4p.png" # Drizzle/Light Rain
    elif 500 <= weather_id <= 531:
        if 'd' in icon_code: icon_file = "7p.png" # Rain Day
        else: icon_file = "2p.png" # Rain Night
    elif 700 <= weather_id <= 781: 
        icon_file = "10p.png" # Mist/Fog
    elif weather_id == 800:
        if 'd' in icon_code: icon_file = "11p.png" # Clear Day
        else: icon_file = "9p.png" # Clear Night
    elif 801 <= weather_id <= 804:
        if 'd' in icon_code: icon_file = "8p.png" # Partly Cloudy Day
        else: icon_file = "3p.png" # Partly Cloudy Night

    try:
        img_path = os.path.join("Assets", icon_file)
        img = Image.open(img_path)
        return customtkinter.CTkImage(img, size=(45, 45))
    except Exception as e:
        print(f"Icon missing: {img_path}")
        return None

# --- Main Logic Function ---
def get_weather():
    city = city_entry.get()

    if not city:
        report_data_label.configure(text="Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        # --- Current Weather ---
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            report_data_label.configure(text="City not found")
            return

        temp = round(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"].title()

        report_data_label.configure(
            text=f"Temperature: {temp}\n"
                 f"Humidity: {humidity}\n"
                 f"Weather: {desc}"
        )

        # Update Recent Searches
        if city not in recent_searches_list:
            recent_searches_list.insert(0, city)
            if len(recent_searches_list) > 5:
                recent_searches_list.pop()
            recent_searches_menu.configure(values=recent_searches_list)
            recent_searches_menu.set("Recent Searches")

        # --- 5-Day Forecast ---
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        
        if str(forecast_data.get("cod")) == "200":
            # API returns data every 3 hours. Step by 8 to get daily data (~24 hours)
            day_index = 0
            for i in range(7, 40, 8):
                if day_index >= 5: # Limit to 5 days
                    break
                    
                day_data = forecast_data["list"][i]
                
                # Format Date (e.g., "31/03")
                date_str = day_data["dt_txt"].split(" ")[0]
                date_formatted = f"{date_str[8:10]}/{date_str[5:7]}"
                
                # Get Temp and Icon
                f_temp = round(day_data["main"]["temp"], 2)
                weather_id = day_data["weather"][0]["id"]
                icon_code = day_data["weather"][0]["icon"]
                
                # Update UI elements
                ctk_icon = get_weather_icon(weather_id, icon_code)
                
                forecast_frames[day_index]["date"].configure(text=date_formatted)
                forecast_frames[day_index]["temp"].configure(text=f"{f_temp} C")
                if ctk_icon:
                    forecast_frames[day_index]["icon"].configure(image=ctk_icon)
                
                day_index += 1

    except Exception as e:
        report_data_label.configure(text="Error fetching weather")
        print(e)

# ==================== UI INTERFACE ====================

# Main Illustration (Right side)
try:
    wheather_img = customtkinter.CTkImage(Image.open("Weather-pana.png"), size=(350, 350))
    wheather_img_lab = customtkinter.CTkLabel(app, image=wheather_img, text="")
    wheather_img_lab.place(x=420, y=50)
except:
    print("Main illustration missing. Continuing without it.")

# Titles (Top Left)
wheather_title = customtkinter.CTkLabel(app, text="WEATHER APP", font=("Helvetica", 34, "normal"))
wheather_title.place(x=30, y=40)

wheather_title_sub = customtkinter.CTkLabel(app, text="Check Wheather without Searching online", font=("Helvetica", 14), text_color="#d1d1d1")
wheather_title_sub.place(x=32, y=80)

# Entry Box (Matches gray box design)
city_entry = customtkinter.CTkEntry(app, 
    placeholder_text="Enter the city name",
    width=240, height=35,
    fg_color="#D9D9D9", placeholder_text_color="#555555",
    text_color="black", border_width=0, corner_radius=0)
city_entry.place(x=32, y=120)

# GET Button (Attached to Entry)
resButton = customtkinter.CTkButton(app, text="", fg_color="#5A5A5A", hover_color="#404040", width=40, height=35, corner_radius=0, command=get_weather)
resButton.place(x=272, y=120)

# Recent Searches Dropdown (Hidden stylishly below entry)
def select_recent_city(choice):
    if choice != "Recent Searches":
        city_entry.delete(0, 'end')
        city_entry.insert(0, choice)
        get_weather() # Automatically fetch when selected

recent_searches_menu = customtkinter.CTkOptionMenu(app, values=["Recent Searches"], width=280, height=28, fg_color="#2b2b2b", button_color="#5A5A5A", command=select_recent_city)
recent_searches_menu.place(x=32, y=165)

# Weather Report Section
wheather_report_title = customtkinter.CTkLabel(app, text="Weather Report :", font=("Helvetica", 22, "normal"))
wheather_report_title.place(x=32, y=220)

report_data_label = customtkinter.CTkLabel(app, 
    text="Temperature: --\nHumidity: --\nWeather: --", 
    font=("Helvetica", 16), justify="left", text_color="#e0e0e0")
report_data_label.place(x=32, y=260)

# Forecast Section
forecast_title = customtkinter.CTkLabel(app, text="5 Days Forecast :", font=("Helvetica", 22, "normal"))
forecast_title.place(x=32, y=400)

# Create 5 blank columns for the forecast icons
forecast_frames = []
for i in range(5):
    # Container for one day
    f_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    f_frame.place(x=45 + (i * 110), y=450) # Horizontal spacing
    
    # Date Label
    lbl_date = customtkinter.CTkLabel(f_frame, text="--/--", font=("Helvetica", 16), text_color="#e0e0e0")
    lbl_date.pack()
    
    # Icon Label
    lbl_icon = customtkinter.CTkLabel(f_frame, text="")
    lbl_icon.pack(pady=8)
    
    # Temperature Label
    lbl_temp = customtkinter.CTkLabel(f_frame, text="-- C", font=("Helvetica", 16), text_color="#b0b0b0")
    lbl_temp.pack()
    
    # Save references so we can update them in get_weather()
    forecast_frames.append({
        "date": lbl_date,
        "icon": lbl_icon,
        "temp": lbl_temp
    })

app.mainloop()
