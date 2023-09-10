import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk

def perform_action():
    selected_option = dropdown_var.get()
    result_label.config(text=f"Select : {selected_option}")

    selected_option = dropdown_var2.get()
    result_label.config(text=f"Select : {selected_option}")

    # result_label.config(text = dropdown_var.get())
    # result_label.config(text = dropdown_var2.get())

root = tk.Tk()
root.title("ai")

label = tk.Label(root, text="เริ่ม",font=("Arial", 25))
label.pack()
photo = tk.PhotoImage(file = "D:\มินิโปรไมโคร\Ai\miniproject_python\img.png")
label3 = tk.Label(root, image=photo)
label3.pack()
dropdown_var = tk.StringVar()
dropdown_var2 = tk.StringVar()
canvas = tk.Canvas(root, width=300, height=50)
canvas.pack()

dropdown = ttk.Combobox(root, textvariable=dropdown_var)
dropdown2 = ttk.Combobox(root, textvariable=dropdown_var2)
dropdown['values'] = ('ต้นไม้1', 'ต้นไม้2', 'ต้นไม้3', 'ต้นไม้4')
dropdown2['values'] = ('ต้นไม้1', 'ต้นไม้2', 'ต้นไม้3', 'ต้นไม้4')
dropdown.pack()
label2 = tk.Label(root, text="to",font=("Arial", 25))
label2.pack()
dropdown2.pack()
action_button = tk.Button(root, text="submit", command=perform_action)
action_button.pack()

result_label = tk.Label(root, text="",font=("Arial", 25))
result_label.pack()

root.mainloop()
