import tkinter as tk
from tkinter import ttk

def on_dropdown_select(event):
    selected_option = dropdown_var.get()
    result_label.config(text=f"Selected: {selected_option}")

root = tk.Tk()
root.title("เลือก")
label = tk.Label(root, text="เลือกต้นไม้:")
label.pack()
dropdown_var = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=dropdown_var)
dropdown['values'] = ('ต้นไม้1', 'ต้นไม้2', 'ต้นไม้3', 'ต้นไม้4')
dropdown.pack()
dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)
result_label = tk.Label(root, text="")
result_label.pack()
button = tk.Button(text = "submit").pack()
root.mainloop()
