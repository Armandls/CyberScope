import socket
from colorama import Fore, Style, init
from utils.utils import print_underline, write_log

def connect_to_server(host, port, really_connect):
    if really_connect == 1:
        print(Fore.RED + "You are already connected to the Honeypot server.🔒🎃" + Style.RESET_ALL)
        return None, really_connect

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)  # Configura un timeout de 5 segundos
    try:
        client_socket.connect((host, port))  # Establece la conexión
        return client_socket, 1
    except ConnectionRefusedError:
        print(Fore.RED + "\nCould not establish connection to the Honeypot server. Verify that it is running." + Style.RESET_ALL)
    except socket.timeout:
        print(Fore.RED + "Connection to the Honeypot server timed out." + Style.RESET_ALL)
    return None, 0

def disconnect_from_server(client_socket):
    try:
        client_socket.sendall("DISCONNECT".encode())  # Envía el mensaje
        print(Fore.RED + "Disconnecting from the Honeypot server." + Style.RESET_ALL)
    except (socket.error, socket.timeout):
        print(Fore.RED + "Error while disconnecting from the Honeypot server." + Style.RESET_ALL)
    finally:
        client_socket.close()  # Cierra el socket

def interact_with_service(client_socket, service_type):
    
    print_underline()
    if service_type == "FTP":
        print(Fore.YELLOW + "\nAvailable commands: LIST, UPLOAD, DOWNLOAD, QUIT" + Style.RESET_ALL)
    elif service_type == "SSH":
        print(Fore.YELLOW + "\nAvailable commands: ls, pwd, exit" + Style.RESET_ALL)
    
    while True:
        command = input(Fore.CYAN + f"\n{service_type}> " + Style.RESET_ALL).strip()
        client_socket.sendall(command.encode())  # Envía el comando al servidor
        
        if command.upper() in ["QUIT", "EXIT"]:
            break
        
        # Recibe la respuesta del servidor
        response = client_socket.recv(4096).decode()
        print(Fore.GREEN + response + Style.RESET_ALL)

# Simulación de servicio FTP
def simulate_ftp(cliente_socket):
    cliente_socket.sendall("Connected to the FTP server simulation.".encode())
    while True:
        command = cliente_socket.recv(1024).decode().strip()
        if command.upper() == "LIST":
            response = "Here comes the directory listing.\nfile1.txt\nfile2.txt\nfile3.txt\n226 Directory send okay."
            print(Fore.MAGENTA + "Directory listing requested." + Style.RESET_ALL)
        elif command.upper() == "UPLOAD":
            response = "File uploaded successfully."
            print(Fore.MAGENTA + "File upload requested." + Style.RESET_ALL)
        elif command.upper() == "DOWNLOAD":
            response = "File downloaded successfully."
            print(Fore.MAGENTA + "File download requested." + Style.RESET_ALL)
        elif command.upper() == "QUIT":
            print(Fore.RED + "Client disconnected from FTP service." + Style.RESET_ALL)
            break
        else:
            response = "Unknown command."
        cliente_socket.sendall((response).encode())

# Simulación de servicio SSH
def simulate_ssh(cliente_socket):
    cliente_socket.sendall("Connected to the SSH server simulation.".encode())
    while True:
        command = cliente_socket.recv(1024).decode().strip()
        if command.lower() == "ls":
            response = "file1.txt\nfile2.txt\nfile3.txt"
            print(Fore.MAGENTA + "Directory listing requested." + Style.RESET_ALL)
        elif command.lower() == "pwd":
            response = "/home/user"
            print(Fore.MAGENTA + "Print working directory requested." + Style.RESET_ALL)
        elif command.lower() == "exit":
            print(Fore.RED + "Client disconnected from SSH service." + Style.RESET_ALL)
            break
        else:
            response = "Unknown command."
        cliente_socket.sendall((response).encode())

# Función para manejar a cada cliente
def handle_client(cliente_socket, direccion_cliente):
    try:
        while True:
            datos = cliente_socket.recv(1024).decode().strip()
            if not datos:
                break

            print(Fore.CYAN + f"\nRequest received from {direccion_cliente}: {datos}" + Style.RESET_ALL)

            if datos.upper() == "CONNECT FTP":
                write_log("SERVICE", f"Client {direccion_cliente} connected to FTP service.")
                simulate_ftp(cliente_socket)
            elif datos.upper() == "CONNECT SSH":
                write_log("SERVICE", f"Client {direccion_cliente} connected to SSH service.")
                simulate_ssh(cliente_socket)
            elif datos.upper() == "DISCONNECT":
                write_log("DISCONNECT", f"Client disconnected: IP:{direccion_cliente[0]}:{direccion_cliente[1]}")
                print(Fore.RED + f"Client {direccion_cliente} disconnected." + Style.RESET_ALL)
                cliente_socket.close()
                break
            else:
                response = "Unknown service. Try CONNECT FTP or CONNECT SSH."
                cliente_socket.sendall((response + "\n").encode())

    except ConnectionResetError:
        print(Fore.RED + f"Connection reset by client: {direccion_cliente}" + Style.RESET_ALL)
    finally:
        cliente_socket.close()
        print(Fore.YELLOW + f"Connection closed with {direccion_cliente}" + Style.RESET_ALL)