import socket
from threading import Thread
from colorama import Fore, Style, init
from datetime import datetime
from communication.communication import handle_client

init()  # Inicializa el módulo colorama

# Función principal para iniciar el servidor
def start_server(host="127.0.0.1", puerto=8080):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        servidor_socket.bind((host, puerto))
        servidor_socket.listen(5)
        print(Fore.YELLOW + f"Server started on {host}:{puerto}. Waiting for connections...\n" + Style.RESET_ALL)
        
        while True:
            cliente_socket, direccion_cliente = servidor_socket.accept()
            cliente_thread = Thread(target=handle_client, args=(cliente_socket, direccion_cliente))
            cliente_thread.start()
    
    except KeyboardInterrupt:
        print(Fore.RED + "Server stopped by user. Exiting..." + Style.RESET_ALL)
    finally:
        servidor_socket.close()
        print(Fore.YELLOW + "Server socket closed. Goodbye!" + Style.RESET_ALL)

if __name__ == "__main__":
    start_server()
