import socket
import threading
from colorama import Fore, Style, init
from datetime import datetime
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import paramiko

init()  # Inicializa colorama

# Función para escribir en el log
def write_log(event_type, message):
    os.makedirs("Logs", exist_ok=True)  # Crea la carpeta si no existe
    with open("Logs/logs.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] EVENT: {event_type} - {message}\n")

# Configuración del servidor FTP
def start_ftp_server():
    authorizer = DummyAuthorizer()
    # Configura un usuario con acceso a un directorio real
    ftp_root = "ftp_root"  # Cambia esto al directorio deseado
    os.makedirs(ftp_root, exist_ok=True)  # Crea el directorio raíz si no existe
    authorizer.add_user("user", "password", ftp_root, perm="elradfmw")  # elradfmw = todos los permisos
    handler = FTPHandler
    handler.authorizer = authorizer

    # Configura y arranca el servidor
    ftp_server = FTPServer(("0.0.0.0", 21), handler)
    print(Fore.YELLOW + "FTP server started on port 21." + Style.RESET_ALL)
    write_log("SERVICE", "FTP server started on port 21.")
    ftp_server.serve_forever()

# Configuración del servidor SSH
def start_ssh_server():
    def handle_ssh_client(client, address):
        transport = paramiko.Transport(client)
        transport.add_server_key(paramiko.RSAKey.generate(2048))

        # Servidor SSH básico con autenticación
        class SimpleSSHServer(paramiko.ServerInterface):
            def check_auth_password(self, username, password):
                if username == "user" and password == "password":
                    return paramiko.AUTH_SUCCESSFUL
                return paramiko.AUTH_FAILED

            def get_allowed_auths(self, username):
                return "password"

            def check_channel_request(self, kind, chanid):
                if kind == "session":
                    return paramiko.OPEN_SUCCEEDED
                return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        server = SimpleSSHServer()
        transport.start_server(server=server)

        try:
            channel = transport.accept(20)  # Espera hasta 20 segundos para aceptar una conexión
            if channel is None:
                print("SSH connection timed out.")
                return

            print(Fore.GREEN + f"SSH client connected: {address}" + Style.RESET_ALL)
            channel.send("Welcome to the SSH Honeypot! Type 'exit' to disconnect.\n")

            while True:
                try:
                    command = channel.recv(1024).decode().strip()
                    if not command:
                        continue

                    if command.lower() == "exit":
                        channel.send("Goodbye!\n")
                        break

                    # Ejecuta el comando y devuelve la salida
                    print(Fore.CYAN + f"Executing command: {command}" + Style.RESET_ALL)
                    result = os.popen(command).read()  # Ejecuta el comando
                    if result:
                        channel.send(result)
                    else:
                        channel.send(f"Command '{command}' executed.\n")
                except Exception as e:
                    print(Fore.RED + f"Error processing SSH command: {e}" + Style.RESET_ALL)
                    channel.send(f"Error executing command: {str(e)}\n")
                    break
        except Exception as e:
            print(Fore.RED + f"Error in SSH client handling: {e}" + Style.RESET_ALL)
        finally:
            transport.close()

    ssh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssh_socket.bind(("0.0.0.0", 22))
    ssh_socket.listen(5)

    print(Fore.YELLOW + "SSH server started on port 22." + Style.RESET_ALL)
    write_log("SERVICE", "SSH server started on port 22.")

    while True:
        client, address = ssh_socket.accept()
        threading.Thread(target=handle_ssh_client, args=(client, address), daemon=True).start()



# Función principal para iniciar el servidor
def start_server():
    ftp_thread = threading.Thread(target=start_ftp_server)
    ssh_thread = threading.Thread(target=start_ssh_server)

    # Inicia los hilos del servidor FTP y SSH
    ftp_thread.start()
    ssh_thread.start()

    print(Fore.YELLOW + "\nFTP and SSH servers are running.\n" + Style.RESET_ALL)

    try:
        ftp_thread.join()  # Espera a que el hilo FTP termine (nunca debería terminar)
        ssh_thread.join()  # Espera a que el hilo SSH termine
    except KeyboardInterrupt:
        print(Fore.RED + "Stopping servers..." + Style.RESET_ALL)
        # Aquí puedes añadir lógica para detener los servidores FTP y SSH si es necesario

if __name__ == "__main__":
    start_server()

