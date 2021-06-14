import pickle
import socket
from player import Player
from game import Game
from _thread import *

server = "10.0.3.1"  # has to be running on this machine
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server started")


players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255)), Player(150,150,50,50,(0,255,0)), Player(200,200,50,50,(255,255,0))]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data
            print("player :", player)

            if not data:
                print("Disconnected")
                break
            else:
                if player == 3:
                    reply = players[0]
                elif player == 2:
                    reply = players[1]
                elif player == 1:
                    reply = players[2]
                else:
                    reply = players[3]

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
