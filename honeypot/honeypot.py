import socket
from colorama import Fore, Style, init
from utils.utils import welcome_message_honeypot

def connect_to_server(host, port, really_connect):
    if really_connect == 1:
        print(Fore.RED + "You are already connected to the Honeypot server.🔒🎃" + Style.RESET_ALL)
        return None, really_connect

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)  # Configura un timeout de 5 segundos
    try:
        client_socket.connect((host, port))
        print(Fore.GREEN + f"Connection established with Honeypot server ({host}:{port})." + Style.RESET_ALL)
        # Envía una solicitud simulada
        client_socket.sendall("CONNECT".encode())
        response = client_socket.recv(4096).decode()  # Recibe la respuesta del servidor
        print(Fore.CYAN + "\nHoneypot Server Response:" + Style.RESET_ALL)
        print(Fore.MAGENTA + response + Style.RESET_ALL)

        return client_socket, 1
    except ConnectionRefusedError:
        print(Fore.RED + "Could not establish connection to the Honeypot server. Verify that it is running." + Style.RESET_ALL)
    except socket.timeout:
        print(Fore.RED + "Connection to the Honeypot server timed out." + Style.RESET_ALL)
    return None, 0

def disconnect_server(client_socket):
    client_socket.sendall("DISCONNECT".encode())  # Envía el mensaje
    client_socket.close()  # Cierra el socket

def connect_honeypot(host="localhost", port=8080):
    client_socket = None  # Inicializa el socket del cliente como None
    really_connect = 0

    welcome_message_honeypot()

    while True:
        print(Fore.YELLOW + "\nSelect one of the following options:\n" + Style.RESET_ALL)
        print("\t1. Connect to Honeypot")
        print("\t2. Exit")
        option_honeypot = input(Fore.CYAN + "\nEnter your choice (1/2): " + Style.RESET_ALL)

        if option_honeypot == "1":
            client_socket, really_connect = connect_to_server(host, port, really_connect)
        elif option_honeypot == "2":
            if really_connect == 1:
                disconnect_server(client_socket)
            else:
                print(Fore.RED + "You are not connected to the Honeypot server." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid option. Please select 1 or 2." + Style.RESET_ALL)

