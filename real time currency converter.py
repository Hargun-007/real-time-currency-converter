import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Currency full names
currency_full_names = {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "INR": "Indian Rupee",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "CNY": "Chinese Yuan",
    "CHF": "Swiss Franc",
    "SGD": "Singapore Dollar",
    "ZAR": "South African Rand",
    "BRL": "Brazilian Real",
    "RUB": "Russian Ruble",
    "KRW": "South Korean Won",
    "NZD": "New Zealand Dollar"
}

def fetch_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data['rates']
    except:
        messagebox.showerror("Error", "Failed to fetch exchange rates")
        return None

def get_code(selection):
    return selection.split(" - ")[0]

def update_live_rate(*args):
    try:
        from_code = get_code(from_currency_cb.get())
        to_code = get_code(to_currency_cb.get())
        if from_code and to_code:
            rate = rates[to_code] / rates[from_code]
            live_rate_label.config(
                text=f"💱 1 {currency_full_names[from_code]} = {rate:.4f} {currency_full_names[to_code]}"
            )
    except:
        live_rate_label.config(text="Error loading rate")

def convert():
    try:
        amount = float(amount_entry.get())
        from_code = get_code(from_currency_cb.get())
        to_code = get_code(to_currency_cb.get())
        rate = rates[to_code] / rates[from_code]
        result = amount * rate
        result_label.config(
            text=f"{amount:.2f} {currency_full_names[from_code]} = {result:.2f} {currency_full_names[to_code]}"
        )
    except:
        messagebox.showerror("Error", "Invalid input or currency")

# GUI setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("600x400")
root.resizable(False, False)

# Fetch exchange rates
rates = fetch_rates()
currency_list = sorted(rates.keys())
dropdown_list = [f"{code} - {currency_full_names.get(code, code)}" for code in currency_list]

# Configure columns for equal width
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

# Row 0: Amount
tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
amount_entry = tk.Entry(root, width=30)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

# Row 1: From Currency
tk.Label(root, text="From Currency:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
from_currency_cb = ttk.Combobox(root, values=dropdown_list, width=30)
from_currency_cb.set("USD - United States Dollar")
from_currency_cb.grid(row=1, column=1, padx=10, pady=10)

# Row 2: To Currency
tk.Label(root, text="To Currency:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
to_currency_cb = ttk.Combobox(root, values=dropdown_list, width=30)
to_currency_cb.set("INR - Indian Rupee")
to_currency_cb.grid(row=2, column=1, padx=10, pady=10)

# Row 3: Live Rate
live_rate_label = tk.Label(root, text="", font=('Arial', 12), fg="blue")
live_rate_label.grid(row=3, column=0, columnspan=2, pady=10)

# Row 4: Convert Button
tk.Button(root, text="Convert", command=convert, width=20).grid(row=4, column=0, columnspan=2, pady=15)

# Row 5: Result
result_label = tk.Label(root, text="", font=('Arial', 14))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# Event bindings
from_currency_cb.bind("<<ComboboxSelected>>", update_live_rate)
to_currency_cb.bind("<<ComboboxSelected>>", update_live_rate)

root.mainloop()
