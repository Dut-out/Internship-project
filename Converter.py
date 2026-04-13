import customtkinter as ctk
import requests
from tkinter import messagebox
from PIL import Image

API_KEY = "a9694d800bff07b5e8cb8275"

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Currency Converter")
app.geometry("750x450")
# Updated to match the forest green background in your design
app.configure(fg_color="#0e7033") 

currencies = [
    "USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"
]

def convert_currency(event=None):
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        data = response.json()

        rate = data["conversion_rates"][to_currency]
        result = amount * rate

        # Update the three result labels
        result_title.configure(text="Currency converted")
        result_path.configure(text=f"{from_currency} -> {to_currency}")
        result_label.configure(
            text=f"{amount} {from_currency} = {result:.2f} {to_currency}"
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
    except KeyError:
        messagebox.showerror("Error", "Invalid currency selected.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch exchange rate\n{e}")

# --- UI Layout ---

# Titles (Centered at the top)
ctk.CTkLabel(app, text="Currency Converter", font=("Arial", 28, "bold"), text_color="white").place(x=225, y=40)
ctk.CTkLabel(app, text="Convert any currency", font=("Arial", 20), text_color="white").place(x=255, y=75)

# --- LEFT SIDE: INPUTS ---

# Amount Entry (Gray box with a darker teal square button on the end)
amount_entry = ctk.CTkEntry(app, 
    placeholder_text="Enter the Amount", 
    width=290, height=35, 
    corner_radius=0, 
    fg_color="#d9d9d9", 
    placeholder_text_color="#555",
    text_color="black",
    border_width=0)
amount_entry.place(x=50, y=140)

amount_entry.bind("<Return>", convert_currency)

# Convert Button (Wide blue button)
ctk.CTkButton(app, text="Convert", command=convert_currency, 
    width=290, height=35, corner_radius=0, 
    fg_color="#1c7ef0", hover_color="#1460bc", text_color="white", font=("Arial", 14)).place(x=50, y=190)

# Results Section
result_title = ctk.CTkLabel(app, text="", font=("Arial", 20, "bold"), text_color="white", width=290)
result_title.place(x=50, y=280)

result_path = ctk.CTkLabel(app, text="", font=("Arial", 18), text_color="white", width=290)
result_path.place(x=50, y=315)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 18), text_color="white", width=290)
result_label.place(x=50, y=350)


# --- RIGHT SIDE: DROPDOWNS & IMAGE ---

# From Currency Dropdown (Blue with dark blue arrow section)
from_currency_var = ctk.StringVar(value="USD")
ctk.CTkOptionMenu(app, 
    values=currencies, variable=from_currency_var, 
    width=135, height=35, corner_radius=0, 
    fg_color="#1c7ef0", button_color="#0632a6", button_hover_color="#031e6b").place(x=390, y=140)

# To Currency Dropdown
to_currency_var = ctk.StringVar(value="INR")
ctk.CTkOptionMenu(app, 
    values=currencies, variable=to_currency_var, 
    width=135, height=35, corner_radius=0, 
    fg_color="#1c7ef0", button_color="#0632a6", button_hover_color="#031e6b").place(x=550, y=140)

# Image setup
try:
    coins_img = ctk.CTkImage(Image.open("Coins-rafiki.png"), size=(250, 250)) 
    img_label = ctk.CTkLabel(app, image=coins_img, text="")
    img_label.place(x=410, y=190)
except FileNotFoundError:
    print("Warning: 'Coins-amico.png' not found in the directory.")

app.mainloop()