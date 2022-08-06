#------------- Boilerplate Code Start------
import socket
from tkinter import *
from  threading import Thread
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None

playerName = None
nameEntry = None
nameWindow = None

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_width
    global screen_height

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas(nameWindow, width = screen_width, height = screen_height)
    canvas1.pack(fill = "both", expand = True)

    canvas1.create_image(screen_width/2, screen_height/2, image=bg, anchor = CENTER)
    canvas1.create_text(screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE", 50), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(relx = 0.5, rely=0.45, anchor=CENTER)

    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(relx=0.5, rely=0.75, anchor=CENTER)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def saveName():
  global SERVER
  global playerName
  global nameWindow
  global nameEntry

  playerName = nameEntry.get()
  SERVER.send(playerName.encode("utf-8"))
  nameWindow.destroy()
  
def setup():
  global SERVER
  global PORT
  global IP_ADDRESS

  PORT  = 5000
  IP_ADDRESS = '127.0.0.1'

  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SERVER.connect((IP_ADDRESS, PORT))

  askPlayerName()

setup()
