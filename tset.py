from tkinter import *

root = Tk()
root.title("tk")

label = Label(text="Hello World")
label2 = Label(text="Hello World2").pack()
button = Button(text = "submit")
label.pack()
button.pack()
root.mainloop()