import socket
from threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None

CLIENTS = {}
playerNames=[]

def acceptConnections():
  global CLIENTS
  global SERVER
  while True:
    player_socket, addr = SERVER.accept()
    try:
      player_name = player_socket.recv(2048).decode().strip()
    except:
      pass
  
    if len(CLIENTS.keys()) == 0:
      CLIENTS[player_name] = {'player_type': 'player1'}
    else:
      CLIENTS[player_name] = {'player_type': 'player2'}

    CLIENTS[player_name]["player_socket"] = player_socket
    CLIENTS[player_name]["address"] = addr
    CLIENTS[player_name]["player_name"] = player_name
    CLIENTS[player_name]["turn"] = False

    print(f"Connection established with {player_name} : {addr}")
    
    thread = Thread(target=handleClients, args=(player_socket, player_name))
    thread.start()

def handleClients(socket, name):
  global CLIENTS
  global playerNames
  
  playerType=CLIENTS[name]["player_type"]
  if(playerType== 'player1'):
    CLIENTS[name]['turn'] = True
    socket.send(str({'player_type': CLIENTS[name]["player_type"], 'turn': CLIENTS[name]['turn'], 'player_name': name}).encode("utf-8"))
  else:
    CLIENTS[name]['turn'] = False
    socket.send(str({'player_type': CLIENTS[name]["player_type"], 'turn': CLIENTS[name]['turn'], 'player_name': name}).encode("utf-8"))
  
  playerNames.append({"name": name, "type": CLIENTS[name]["player_type"]})
  
  if len(playerNames) > 0 and len(playerNames) <= 2:
    for cName in CLIENTS:
      cSocket = CLIENTS[cName]["player_socket"]
      cSocket.send(str({"player_names": playerNames}).encode('utf-8'))
       
  while True:
    try:
      message = socket.recv(2048)
      if(message):
        for cName in CLIENTS:
          cSocket = CLIENTS[cName]["player_socket"]
          cSocket.send(message)
    except:
      pass

def setup():
  print("\n")
  print("\t\t\t\t\t\t*** LUDO LADDER ***\n")
  global SERVER
  global PORT
  global IP_ADDRESS
  IP_ADDRESS = '127.0.0.1'
  PORT = 5000
  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SERVER.bind((IP_ADDRESS, PORT))
  SERVER.listen(10)
  print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")
  acceptConnections()

setup()
