import tkinter as tk
import tkinter.font as tkFont
import pathlib

def close_window():
    window.destroy()

window = tk.Tk()
window.title('Eye Scan')
window.geometry('220x100+0+0')
window.resizable(False, False)
window.eval('tk::PlaceWindow . center')
fontStyle2 = tkFont.Font(family="Arial Unicode MS", size=10)
button = tk.Button(text="Press Buttom \n( Stop Auto Eye Scan )", command=close_window, font=('Arial',10,'bold'), padx=10, pady=10, bg='#f90', bd=5)

from tkinter.constants import CENTER #加到第一行

button.place(x=110,y=50,anchor=CENTER)

window.mainloop()




# PyInstaller -F -w event.py