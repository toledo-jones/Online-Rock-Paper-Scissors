import pickle
import socket
from _thread import *
from game import Game

SERVER = "192.168.1.149"
PORT = 5555
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    SOCKET.bind((SERVER, PORT))
except socket.error as e:
    print(e)

SOCKET.listen()
print('Server Started')
print('Rock Paper Scissors v.01')
print('Waiting for Connection...')

connected = set()
games = {}
id_count = 0


def threaded_client(connection, player, game_id):
    # Continuously runs for each connected client

    global id_count
    connection.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = connection.recv(4096).decode()
            # If you run out of memory, double this value ^

            # Check to see if the game still exists
            if game_id in games:
                game = games[game_id]

                # Handle received data here
                # Preferably not in a giant if statement...
                if not data:
                    break
                else:
                    # First check to see if we need to reset
                    if data == 'reset':
                        game.reset_selected()
                    # Must be a move
                    elif data != "get":
                        game.play(player, data)
                    # Send the game object
                    reply = game
                    connection.sendall(pickle.dumps(reply))
            else:
                break
        except:     # Again with this?
            break

    print("Lost Connection")
    try:
        del games[game_id]
        print(f"Closing Game: {game_id}")
    except:     # Handle this more precisely in the future
        pass
    id_count -= 1
    connection.close()


while True:
    connection, address = SOCKET.accept()
    print(f"Connected to {address}")
    id_count += 1
    player = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print(f"Creating a new game...")
        print(f'ID: {game_id}')
        print('...')
    else:
        games[game_id].set_ready(True)
        player = 1

    start_new_thread(threaded_client, (connection, player, game_id))