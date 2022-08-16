import socket, random
from tkinter import *
from  threading import Thread
from PIL import ImageTk

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None
canvas2 = None
nameEntry = None
playerName = None
nameWindow = None
gameWindow = None

player1Name = 'joining'
player2Name = 'joining'
player1Label = None
player2Label = None

player1Score = 0 
player2Score = 0
player1ScoreLabel = None
player2ScoreLabel = None

dice = None
rollBtn = None
resetBtn = None
playerType = None
playerTurn = None
finishingBox = None

winningMsg = None
winingFunctionCall = 0

leftBoxes = []
rightBoxes = []

def checkColorPosition(boxes, color):
  for box in boxes: 
    boxColor = box.cget("bg")
    if(boxColor == color):
      return boxes.index(box)
    return False

def movePlayer1(steps):
  global leftBoxes, finishingBox, SERVER, playerName
  boxPosition = checkColorPosition(leftBoxes[1:], "red")
  if boxPosition:
    diceValue = steps
    coloredBoxIndex = boxPosition
    totalSteps = 10
    remainingSteps = totalSteps - steps

    if steps == remainingSteps:
      for box in leftBoxes[1:]:
        box.configure(bg = "white")
      finishingBox.configure(bg = "red")

      greetmsg = 'Red wins the game.'
      SERVER.send(greetmsg.encode('utf-8'))

    elif steps < remainingSteps:
      for box in leftBoxes[1:]:
        box.configure(bg = "white")
      nextStep = (coloredBoxIndex + 1) + diceValue
      leftBoxes[nextStep].configure(bg = "red")

    else:
      print("Wrong Move")
    
  else:
    leftBoxes[steps - 1].configure(bg = "red")

def movePlayer2(steps):
  global rightBoxes, finishingBox
  tempBoxes = rightBoxes[-2::-1]
  boxPosition = checkColorPosition(tempBoxes, "yellow")
  if boxPosition:
    diceValue = steps
    coloredBoxIndex = boxPosition
    totalSteps = 10
    remainingSteps = totalSteps - steps

    if diceValue == remainingSteps:
      for box in tempBoxes:
        box.configure(bg="white")
      finishingBox.configure(bg="yellow")
      SERVER.send("Yellow wins the game".encode("utf-8"))

    elif diceValue < remainingSteps:
      for box in tempBoxes:
        box.configure(bg="white")
      nextStep = (boxPosition+1) - diceValue
      tempBoxes[nextStep].configure(bg="yellow")
      
    else:
      print("Wrong move")

  else:
    rightBoxes[-1*steps].configure(bg="yellow")

def askPlayerName():
  global playerName, nameEntry, nameWindow, canvas1, screen_width, screen_height

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
  global SERVER, playerType, rollBtn, playerTurn

  diceChoices=["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
  value = random.choice(diceChoices)

  rollBtn.destroy()
  playerTurn = False

  if playerType == "player1":
    SERVER.send(f"{value}player2-turn".encode("utf-8"))
  elif playerType == "player2":
    SERVER.send(f"{value}player1-turn".encode("utf-8"))

def createFinishingBox():
  global finishingBox, gameWindow, screen_width, screen_height

  finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 25), width=6, height=3, borderwidth=0, bg="green", fg="white")
  finishingBox.place(x=screen_width/2 - 60, y=screen_height/2 - 115)

def rightBoard():
  global gameWindow, rightBoxes, screen_height

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
    rollBtn.place(x = screen_width/2, y = (screen_height/2)+150, anchor=CENTER)
  else:
    print("Dice not visible")
    rollBtn.pack_forget()

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


def restGame():
  global SERVER
  SERVER.send("reset game".encode())

def handleResetGame():
  global canvas2
  global playerType
  global gameWindow
  global rollBtn
  global dice
  global screen_width
  global screen_height
  global playerTurn
  global rightBoxes
  global leftBoxes
  global finishingBox
  global resetBtn
  global winningMsg
  global winingFunctionCall

  canvas2.itemconfigure(dice, text='\u2680')

  # Handling Reset Game
  if playerType == 'player1':
    rollBtn = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey", command=rollDice, width=20, height=5)
    rollBtn.place(x=screen_width / 2 - 80, y=screen_height/2  + 150)
    playerTurn = True

  if playerType == 'player2':
    playerTurn = False

  for rBox in rightBoxes[-2::-1]:
    rBox.configure(bg='white')

  for lBox  in leftBoxes[1:]:
    lBox.configure(bg='white')

  finishingBox.configure(bg='green')
  canvas2.itemconfigure(winningMsg, text="")
  resetBtn.destroy()

  # Again Recreating Reset Button for next game
  resetBtn =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)
  winingFunctionCall = 0

def receivedMsg():
  global SERVER, playerType, playerTurn, rollBtn, screen_height, screen_width
  global canvas2, dice, gameWindow, player1Name, player2Name, player1Label
  global player2Label, winingFunctionCall

  while True:
    message = SERVER.recv(2048).decode()

    if 'player_type' in message:
      recvMsg = eval(message)
      playerType = recvMsg['player_type']
      playerTurn = recvMsg['turn']

    elif 'player_names' in message:
      players = eval(message)
      players = players["player_names"]
      for p in players:
        if p["type"] == 'player1':
          player1Name = p['name']
        if p["type"] == 'player2':
          player2Name = p['name']

    elif ('⚀' in message):
      canvas2.itemconfigure(dice, text = '\u2680')
    elif ('⚁' in message):
      canvas2.itemconfigure(dice, text = '\u2681')
    elif ('⚂' in message):
      canvas2.itemconfigure(dice, text = '\u2682')
    elif ('⚃' in message):
      canvas2.itemconfigure(dice, text = '\u2683')
    elif ('⚄' in message):
      canvas2.itemconfigure(dice, text = '\u2684')
    elif ('⚅' in message):
      canvas2.itemconfigure(dice, text = '\u2685')
    elif ('wins the game.' in message and winingFunctionCall == 0):
      winingFunctionCall +=1
      handleWin(message)
      
    elif (message == 'reset game'):
      handleResetGame()

    if ('player1Turn' in message and playerType == 'player1'):
      playerTurn = True
      rollBtn = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
      rollBtn.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

    elif ('player2Turn' in message and playerType == 'player2'):
      playerTurn = True
      rollBtn = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
      rollBtn.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

    if ('player1Turn' in message or 'player2Turn' in message):
      diceChoices = ['⚀','⚁','⚂','⚃','⚄','⚅']
      diceValue = diceChoices.index(message[0]) 

      if('player2Turn' in message):
        movePlayer2(diceValue)
      
      elif('player1Turn' in message):
        movePlayer1(diceValue)

def handleWin(msg):
  global gameWindow, dice, rollBtn, resetBtn, canvas2
  rollBtn.destroy()
  dice.destroy()
  message = msg.split(".")[0] + "."
  canvas2.itemconfigure(winningMsg, text = message)
  resetBtn.place(relx=0.5, rely=0.7, anchor=CENTER)

def setup():
  global SERVER, PORT, IP_ADDRESS

  PORT = 5000
  IP_ADDRESS = '127.0.0.1'

  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SERVER.connect((IP_ADDRESS, PORT))

  thread = Thread(target = receivedMsg)
  thread.start()

  askPlayerName()

setup()
