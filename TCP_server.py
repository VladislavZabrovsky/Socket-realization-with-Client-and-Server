import socket
import numpy as np
import logging
from datetime import datetime


logging.basicConfig(filename='server_log.txt',filemode='w', level=logging.INFO, format='%(message)s')

def create_board():
    return np.full((5, 5), '-')

def check_make_move(board, row, col):
    if 0 <= row <= 4 and 0 <= col <= 4 and board[row][col] == '-':
        return True
    else:
        return False

def place_random_O(board):
    empty_cells = [(i, j) for i in range(5) for j in range(5) if board[i][j] == '-']
    if empty_cells:
        index = np.random.choice(len(empty_cells))
        row, col = empty_cells[index]

        board[row][col] = 'O'

def server_program():
    host = socket.gethostname()
    port = 1037

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Waiting for connection from the client...")
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    board = create_board()

    while True:
        data = conn.recv(256).decode()

        current_time = datetime.now().strftime('[%Y-%m-%d - %H:%M:%S]')

        if data.lower().strip() == "who":
            user_info = "Author: Vladislav Zabrovsky, Variant 12 - Tic-Tac-Toe game"
            conn.send(user_info.encode())
            print("User asked info about labwork")
            logging.info(f"{current_time} - INFO - User asked info about labwork")

        elif data.lower().strip() == "quit":
            print("Client quit the game")
            logging.info(f"{current_time} - INFO - Client quit the game")
            break

        else:
            try:
                row, col = map(int, data.split())
                if check_make_move(board, row, col):
                    print("User committed a move")
                    logging.info(f"{current_time} - INFO - User committed a move")
                    board[row][col] = 'X'

                    place_random_O(board)

                    conn.send(np.array_str(board).encode())
                    print("Server committed a move")
                    logging.info(f"{current_time} - INFO - Server committed a move")

                else:
                    response = "Invalid move. Cell is already occupied or doesn't exist."
                    conn.send(response.encode())
                    print("User committed an invalid move")
                    logging.info(f"{current_time} - INFO - User committed an invalid move")
            except ValueError:
                response = "Invalid input. Please enter row and column (e.g., '2 3')."
                conn.send(response.encode())
                print("User committed an invalid move")
                logging.info(f"{current_time} - INFO - User committed an invalid move")

    conn.close()

if __name__ == '__main__':
 try:
    server_program()
 except Exception as e:
    print(f'Oooops....,smth went wrong - {e}')
