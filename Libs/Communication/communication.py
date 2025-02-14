import os
import socket
from colorama import Fore, Style
from ftplib import FTP
import paramiko

def connect_to_server(host, port, really_connect):
    if really_connect == 1:
        print(Fore.RED + "You are already connected to the Honeypot server. 🔒🎃" + Style.RESET_ALL)
        return None, really_connect

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5) 
    try:
        client_socket.connect((host, port)) 
        print(Fore.GREEN + f"Connected to the Honeypot server at {host}:{port}." + Style.RESET_ALL)
        return client_socket, 1
    except ConnectionRefusedError:
        print(Fore.RED + "Could not connect to the Honeypot server. Is it running?" + Style.RESET_ALL)
    except socket.timeout:
        print(Fore.RED + "Connection to the Honeypot server timed out." + Style.RESET_ALL)
    return None, 0

def disconnect_from_server(client_socket):
    try:
        client_socket.sendall("DISCONNECT".encode())
        print(Fore.RED + "Disconnecting from the Honeypot server." + Style.RESET_ALL)
    except (socket.error, socket.timeout):
        print(Fore.RED + "Error while disconnecting from the Honeypot server." + Style.RESET_ALL)
    finally:
        client_socket.close() 

def connect_ftp_server(host, port, username, password):
    try:
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(user=username, passwd=password)
        print(Fore.LIGHTGREEN_EX + "\nConnected to FTP server." + Style.RESET_ALL)

        while True:
            command = input(Fore.CYAN + "\nFTP> " + Style.RESET_ALL).strip()
            if command.lower() == "quit":
                print(Fore.LIGHTRED_EX + "Exiting FTP session." + Style.RESET_ALL)
                ftp.quit()
                break
            elif command.lower() == "ls":
                ftp.retrlines("LIST")
            elif command.lower().startswith("get "):
                filename = command.split(" ", 1)[1]
                local_path = os.path.join("Files", filename)
                with open(local_path, "wb") as file:
                    ftp.retrbinary(f"RETR {filename}", file.write)
                print(Fore.GREEN + f"Downloaded {filename} to {local_path}" + Style.RESET_ALL)
            elif command.lower().startswith("put "):
                filename = command.split(" ", 1)[1]
                local_path = os.path.join("Files", filename)
                if os.path.exists(local_path):
                    with open(local_path, "rb") as file:
                        ftp.storbinary(f"STOR {filename}", file)
                    print(Fore.GREEN + f"Uploaded {filename} from {local_path}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f"File {filename} not found in Files directory." + Style.RESET_ALL)
            else:
                print(Fore.LIGHTRED_EX + "Unknown FTP command." + Style.RESET_ALL)
    except Exception:
        print(Fore.LIGHTRED_EX + f"\nError connecting to FTP server." + Style.RESET_ALL)
