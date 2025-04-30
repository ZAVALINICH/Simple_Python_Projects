import tkinter as tk
from tkinter import ttk

LARGE_FONT_STYLE = ("Arial", 32, "bold")
SMALL_FONT_STYLE = ("Arial", 14)
DIGITS_FONT_STYLE = ("Arial", 20, "bold")
DEFAULT_FONT_STYLE = ("Arial", 18)

LIGHT_THEME = {
    "background": "#F5F5F5",
    "button": "#FFFFFF",
    "label": "#25265E",
    "history_bg": "#FFFFFF"
}

DARK_THEME = {
    "background": "#2E2E2E",
    "button": "#3C3C3C",
    "label": "#F1F1F1",
    "history_bg": "#1C1C1C"
}

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("420x800")
        self.window.minsize(300, 600)

        self.total_expression = ""
        self.current_expression = ""
        self.history = []
        self.theme = LIGHT_THEME

        self.create_widgets()
        self.apply_theme()

    def apply_theme(self):
        bg = self.theme['background']
        btn = self.theme['button']
        fg = self.theme['label']

        self.display_frame.config(bg=bg)
        self.total_label.config(bg=bg, fg=fg)
        self.label.config(bg=bg, fg=fg)
        self.history_frame.config(bg=bg)
        self.history_listbox.config(bg=self.theme['history_bg'], fg=fg)
        self.converter_frame.config(bg=bg)

        for widget in self.buttons_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=btn, fg=fg)

        for widget in self.converter_frame.winfo_children():
            if isinstance(widget, (tk.Button, tk.Label, ttk.Combobox, tk.Entry)):
                try:
                    widget.config(bg=btn, fg=fg)
                except:
                    pass

    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        self.apply_theme()

    def create_widgets(self):
        self.display_frame = tk.Frame(self.window, height=100)
        self.display_frame.pack(expand=True, fill="both")

        self.total_label = tk.Label(self.display_frame, text=self.total_expression, anchor="e", font=SMALL_FONT_STYLE)
        self.total_label.pack(expand=True, fill="both")

        self.label = tk.Label(self.display_frame, text=self.current_expression, anchor="e", font=LARGE_FONT_STYLE)
        self.label.pack(expand=True, fill="both")

        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(expand=True, fill="both")

        self.create_buttons()
        self.create_history_panel()
        self.create_converter_section()
        self.create_theme_button()

    def create_theme_button(self):
        theme_button = tk.Button(self.window, text="Toggle Theme", font=DEFAULT_FONT_STYLE,
                                 command=self.toggle_theme)
        theme_button.pack(fill='x')

    def create_buttons(self):
        buttons = [
            ("C", 1, 0, self.clear), ("x²", 1, 1, self.square), ("√x", 1, 2, self.sqrt), ("÷", 1, 3, lambda: self.append_operator("/")),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("×", 2, 3, lambda: self.append_operator("*")),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3, lambda: self.append_operator("-")),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3, lambda: self.append_operator("+")),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2, self.evaluate, 2)
        ]

        for (text, row, col, *cmd) in buttons:
            colspan = 1
            if cmd and isinstance(cmd[-1], int):
                colspan = cmd.pop()
            action = cmd[0] if cmd else lambda x=text: self.add_to_expression(x)
            btn = tk.Button(self.buttons_frame, text=text, font=DIGITS_FONT_STYLE, borderwidth=0, command=action)
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew")

        for i in range(6):
            self.buttons_frame.rowconfigure(i, weight=1)
            for j in range(4):
                self.buttons_frame.columnconfigure(j, weight=1)

    def create_history_panel(self):
        self.history_frame = tk.Frame(self.window)
        self.history_frame.pack(fill='both', expand=False)

        history_label = tk.Label(self.history_frame, text="History:", font=SMALL_FONT_STYLE)
        history_label.pack(anchor="w", padx=5)

        self.history_listbox = tk.Listbox(self.history_frame, height=5)
        self.history_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def create_converter_section(self):
        self.converter_frame = tk.Frame(self.window)
        self.converter_frame.pack(fill='both', expand=False, pady=10)

        tk.Label(self.converter_frame, text="Converter:", font=SMALL_FONT_STYLE).grid(row=0, column=0, sticky="w")
        self.input_value = tk.Entry(self.converter_frame)
        self.input_value.grid(row=1, column=0, padx=5, pady=5)

        self.convert_type = ttk.Combobox(self.converter_frame, values=["Data (MB/GB)", "Speed (km/h → m/s)", "Temp (C → F)", "Area (m² → ft²)"])
        self.convert_type.grid(row=1, column=1, padx=5, pady=5)
        self.convert_type.set("Data (MB/GB)")

        self.result_label = tk.Label(self.converter_frame, text="Result: -", font=SMALL_FONT_STYLE)
        self.result_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        convert_btn = tk.Button(self.converter_frame, text="Convert", command=self.convert_units)
        convert_btn.grid(row=1, column=2, padx=5, pady=5)

    def convert_units(self):
        try:
            value = float(self.input_value.get())
            conversion = self.convert_type.get()
            if conversion == "Data (MB/GB)":
                result = f"{value} MB = {value / 1024:.2f} GB"
            elif conversion == "Speed (km/h → m/s)":
                result = f"{value} km/h = {value / 3.6:.2f} m/s"
            elif conversion == "Temp (C → F)":
                result = f"{value}°C = {(value * 9/5) + 32:.2f}°F"
            elif conversion == "Area (m² → ft²)":
                result = f"{value} m² = {value * 10.7639:.2f} ft²"
            else:
                result = "Unknown conversion"
            self.result_label.config(text=f"Result: {result}")
        except ValueError:
            self.result_label.config(text="Invalid input")

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def append_operator(self, operator):
        self.total_expression += self.current_expression + operator
        self.current_expression = ""
        self.update_label()
        self.update_total_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def square(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}**2"))
            self.update_label()
        except:
            self.current_expression = "Error"
            self.update_label()

    def sqrt(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}**0.5"))
            self.update_label()
        except:
            self.current_expression = "Error"
            self.update_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        try:
            result = str(eval(self.total_expression))
            self.history.append(f"{self.total_expression} = {result}")
            self.history_listbox.insert(tk.END, self.history[-1])
            self.current_expression = result
            self.total_expression = ""
        except:
            self.current_expression = "Error"
        self.update_label()
        self.update_total_label()

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    Calculator().run()
#A calculator with a clean Tkinter interface.
#Supports basic arithmetic, square/sqrt, live history, dark/light themes, and unit conversions.

#Features

#Basic math operations (+, -, ×, ÷)

#Square and square root functions

#Resizable GUI

#Light/Dark theme toggle

#Calculation history log

#Unit converter for:

#Data (MB ↔ GB)

#Speed (km/h → m/s)

#Temperature (°C → °F)

#Area (m² → ft²)
#Run It

#python your_file_name.py
