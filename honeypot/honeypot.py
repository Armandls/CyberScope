from colorama import Fore, Style, init
from utils.utils import welcome_message_honeypot, print_underline
from communication.communication import connect_to_server, disconnect_from_server, interact_with_service

def connect_honeypot(host="localhost", port=8080):
    client_socket = None  # Inicializa el socket del cliente como None
    really_connect = 0
    service_option = 0

    welcome_message_honeypot()

    client_socket, really_connect = connect_to_server(host, port, really_connect)

    if client_socket:  # Si la conexión se establece correctamente
        while service_option != "3":
            print_underline()
            print(Fore.YELLOW + "\nSelect a service:\n" + Style.RESET_ALL)
            print("\t1. FTP")
            print("\t2. SSH")
            print("\t3. Disconnect from service")
            
            service_option = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)

            if service_option == "1":
                client_socket.sendall("CONNECT FTP".encode())
                response = client_socket.recv(4096).decode()
                print("\n" + Fore.GREEN + response + Style.RESET_ALL)
                interact_with_service(client_socket, "FTP")
            elif service_option == "2":
                client_socket.sendall("CONNECT SSH".encode())
                response = client_socket.recv(4096).decode()
                print("\n" + Fore.GREEN + response + Style.RESET_ALL)
                interact_with_service(client_socket, "SSH")
            elif service_option == "3":
                client_socket.sendall("DISCONNECT".encode())
                print(Fore.RED + "\nDisconnecting from the Honeypot server." + Style.RESET_ALL)
                client_socket.close()
                return
    if really_connect == 1:
        print(Fore.RED + "You are already connected to the Honeypot server.🔒🎃" + Style.RESET_ALL)
        disconnect_from_server(client_socket)
    else:
        print(Fore.RED + "Try again later.🔒🎃" + Style.RESET_ALL)
        
