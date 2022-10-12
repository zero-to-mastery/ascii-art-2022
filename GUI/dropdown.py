from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog as fd

LIST = ["M.C.", "B.C.", "M.K.C", "M.K.A.", "BSDK"]

root = Tk()
root.title('Slider')
#root.iconbitmap()
root.geometry("640x480")

def show():
    Label(root, text=click.get()).pack()

click =StringVar()
click.set(LIST[0])

drop = OptionMenu(root, click, *LIST).pack()

btn = Button(root, text = "Selection", command=show).pack()

root.mainloop()