
import requests
import customtkinter
from PIL import Image

app = customtkinter.CTk()
app.geometry("600x400")
app.title("Wheather App")

API_KEY = enter api key

#function

def get_weather():
    city = city_entry.get()

    if not city:
        wheather_report.configure(text="Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            wheather_report.configure(text="City not found ")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"].title()

        wheather_report.configure(
            text=f" Temperature: {temp} °C\n"
                 f" Humidity: {humidity}%\n"
                 f" Weather: {desc}"
        )

    except:
        wheather_report.configure(text="Error fetching weather")


#ui interface

wheather_img = customtkinter.CTkImage(
    Image.open("Weather-pana.png"),
    size=(350,350))
wheather_img_lab = customtkinter.CTkLabel(app,image=wheather_img,text="")
wheather_img_lab.place(x=247,y=25)

#text styling
wheather_title =  customtkinter.CTkLabel(app,
    text="Wheater App",
    font=("Arial",32))
wheather_title_sub =  customtkinter.CTkLabel(app,
    text="Check Wheather without Searching online",
    font=("Arial",14))
wheather_report_title =  customtkinter.CTkLabel(app,
    text="Wheater Report:",
    font=("Arial",16))
wheather_report =  customtkinter.CTkLabel(app,
    text="Please enter a city name",
    font=("Arial",14))

#entry box
city_entry = customtkinter.CTkEntry(master=app
    ,placeholder_text="Enter the city name",
    width=200,
    height=30,
    fg_color="white",
    placeholder_text_color="black",
    text_color="black")

city_entry.place(x=12,y=130)

#button placing

resButton = customtkinter.CTkButton(master=app,
    text="GET",
    width=40,
    height=30,
    command=get_weather)

resButton.place(x=210,y=130)

#text placing
wheather_title.place(x=11,y=68)
wheather_title_sub.place(x=11,y=102)
wheather_report_title.place(x=11,y=200)
wheather_report.place(x=11,y=237)

app.mainloop()
