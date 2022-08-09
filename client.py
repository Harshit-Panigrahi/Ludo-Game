import socket, random
from tkinter import *
from  threading import Thread
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None
canvas2 = None
playerName = None
nameEntry = None
nameWindow = None
gameWindow = None
dice = None
finishingBox = None
rollBtn = None
playerType = None
playerTurn = None

leftBoxes = []
rightBoxes = []

def askPlayerName():
  global playerName
  global nameEntry
  global nameWindow
  global canvas1
  global screen_width
  global screen_height

  nameWindow  = Tk()
  nameWindow.title("Ludo Ladder")
  nameWindow.state("zoomed")

  screen_width = nameWindow.winfo_screenwidth()
  screen_height = nameWindow.winfo_screenheight()

  bg = ImageTk.PhotoImage(file = "./assets/background.png")

  canvas1 = Canvas(nameWindow, width = screen_width, height = screen_height)
  canvas1.pack(fill = "both", expand = True)

  canvas1.create_image(screen_width/2, screen_height/2, image=bg, anchor = CENTER)
  canvas1.create_text(screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE", 50), fill="white")

  nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
  nameEntry.place(relx = 0.5, rely=0.45, anchor=CENTER)

  button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30), width=15, command=saveName, height=2, bg="#80deea", bd=3)
  button.place(relx=0.5, rely=0.75, anchor=CENTER)

  nameWindow.resizable(True, True)
  nameWindow.mainloop()

def rollDice():
  global SERVER
  global playerType
  global rollBtn
  global playerTurn

  diceChoices=["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
  value = random.choice(diceChoices)

  rollBtn.destroy()
  playerTurn = False

  if playerType == "player1":
    SERVER.send(f"{value}player2-turn".encode("utf-8"))
  elif playerType == "player2":
    SERVER.send(f"{value}player1-turn".encode("utf-8"))

def createFinishingBox():
  global finishingBox
  global gameWindow
  global screen_width
  global screen_height

  finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 25), width=6, height=3, borderwidth=0, bg="green", fg="white")
  finishingBox.place(x=screen_width/2 - 60, y=screen_height/2 - 115)

def rightBoard():
  global gameWindow
  global rightBoxes
  global screen_height

  xPos = 700
  for box in range(10):
    if box == 9:
      boxLabel = Label(gameWindow, font = ("Helvetica", 30), width = 2, height = 1, borderwidth=2, bg = "yellow", relief = 'ridge')
      boxLabel.place(x = xPos, y = screen_height / 2 - 100)
      rightBoxes.append(box)
      xPos += 55

    else:
      boxLabel = Label(gameWindow, font = ("Helvetica", 30), width = 2, height = 1, borderwidth=2, bg = "white", relief = 'ridge')
      boxLabel.place(x = xPos, y = screen_height / 2 - 100)
      rightBoxes.append(box)
      xPos += 55

def leftBoard():
  global gameWindow
  global leftBoxes
  global screen_height

  xPos = 30
  for box in range(10):
    if box == 0:
      boxLabel = Label(gameWindow, font = ("Helvetica", 30), width = 2, height = 1, borderwidth=2, bg = "red", relief = 'ridge')
      boxLabel.place(x = xPos, y = screen_height / 2 - 100)
      rightBoxes.append(box)
      xPos += 55

    else:
      boxLabel = Label(gameWindow, font = ("Helvetica", 30), width = 2, height = 1, borderwidth=2, bg = "white", relief = 'ridge')
      boxLabel.place(x = xPos, y = screen_height / 2 - 100)
      rightBoxes.append(box)
      xPos += 55

def createGameWindow():
  global gameWindow
  global canvas2
  global dice
  global screen_height
  global screen_width
  global rollBtn
  global playerTurn
  global playerType
  global playerName

  gameWindow = Tk()
  gameWindow.title("Ludo Ladder")
  gameWindow.state("zoomed")

  screen_width = gameWindow.winfo_screenwidth()
  screen_height = gameWindow.winfo_screenheight()

  bg = ImageTk.PhotoImage(file = "./assets/background.png")

  canvas2 = Canvas(gameWindow, width = screen_width, height = screen_height)
  canvas2.pack(fill = "both", expand = True)

  canvas2.create_image(screen_width/2, screen_height/2, image=bg, anchor = CENTER)
  canvas2.create_text(screen_width/2, screen_height/6, text = "Ludo Ladder", font=("Chalkboard SE", 50), fill="white")

  # Calling leftboard and rightboard functions
  leftBoard()
  rightBoard()
  createFinishingBox()

  # creating dice and rollBtn
  dice = canvas2.create_text(screen_width/2, screen_height/2 + 120, text = "\u2680", font=("Chalkboard SE", 200), fill="white", anchor=CENTER)
  rollBtn = Button(gameWindow, text="Roll Dice", bg="grey", font=("Chalkboard SE", 20), width=20, height=5, command=rollDice)
  if playerType == "player1" and playerTurn:
    rollBtn.place(screen_width/2, screen_height/2 + 300)
  else:
    rollBtn.pack_forget()

  gameWindow.resizable(True, True)
  gameWindow.mainloop()

def saveName():
  global SERVER
  global playerName
  global nameWindow
  global nameEntry

  playerName = nameEntry.get()
  SERVER.send(playerName.encode("utf-8"))
  nameWindow.destroy()

  #calling the game window
  createGameWindow()

def setup():
  global SERVER
  global PORT
  global IP_ADDRESS

  PORT = 5000
  IP_ADDRESS = '127.0.0.1'

  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SERVER.connect((IP_ADDRESS, PORT))

  askPlayerName()

setup()
