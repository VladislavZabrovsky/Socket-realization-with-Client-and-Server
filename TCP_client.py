import socket
import logging
from datetime import datetime


logging.basicConfig(filename='client_log.txt',filemode='w', level=logging.INFO, format='%(message)s')

def client_program():
    host = socket.gethostname()
    port = 1037

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Enter row and column (e.g., '2 3'), Who, or Quit: ").strip()

        client_socket.send(message.encode())
        data = client_socket.recv(256).decode()

        current_time = datetime.now().strftime('[%Y-%m-%d] %H:%M:%S')
        logging.info(f"{current_time} - INFO - Sent: {message}")
        logging.info(f"{current_time} - INFO - Received: {data}")
        print(data)
        if message.lower() == 'quit':
            print('End of the game')
            logging.info(f"{current_time} - INFO - End of the game")
            break

    client_socket.close()

if __name__ == '__main__':
 try:
    client_program()
 except Exception as e:
    print(f'Oooops....,smth went wrong - {e}')
