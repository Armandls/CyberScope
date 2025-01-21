import socket
import threading
from colorama import Fore, Style, init
from datetime import datetime
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

init()  # Inicializa colorama

# Función para escribir en el log
def write_log(event_type, message):
    os.makedirs("Logs", exist_ok=True)  # Crea la carpeta si no existe
    with open("Logs/logs.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] EVENT: {event_type} - {message}\n")

# Clase personalizada para manejar eventos del servidor FTP
class CustomFTPHandler(FTPHandler):
    def on_connect(self):
        """Se llama cuando un cliente se conecta al servidor."""
        client_info = f"{self.remote_ip}:{self.remote_port}"
        write_log("CONNECT", f"Client connected: {client_info}")

    def on_disconnect(self):
        """Se llama cuando un cliente se desconecta del servidor."""
        client_info = f"{self.remote_ip}:{self.remote_port}"
        write_log("DISCONNECT", f"Client disconnected: {client_info}")

    def on_login(self, username):
        """Se llama cuando un usuario inicia sesión correctamente."""
        write_log("LOGIN", f"User logged in: {username}")

    def on_logout(self, username):
        """Se llama cuando un usuario cierra sesión."""
        write_log("LOGOUT", f"User logged out: {username}")

# Configuración del servidor FTP
def start_ftp_server():
    authorizer = DummyAuthorizer()
    ftp_root = "ftp_root"  # Directorio raíz del servidor FTP
    os.makedirs(ftp_root, exist_ok=True)  # Crea el directorio si no existe
    authorizer.add_user("user", "password", ftp_root, perm="elradfmw")  # Usuario FTP

    handler = CustomFTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer(("0.0.0.0", 21), handler)
    print(Fore.YELLOW + "\nFTP server is running on port 21.\n" + Style.RESET_ALL)
    write_log("SERVICE", "FTP server started on port 21.")
    ftp_server.serve_forever()

# Función principal para iniciar el servidor FTP
def start_server():
    ftp_thread = threading.Thread(target=start_ftp_server, daemon=True)
    ftp_thread.start()

    try:
        ftp_thread.join()
    except KeyboardInterrupt:
        print(Fore.RED + "Stopping FTP server..." + Style.RESET_ALL)

if __name__ == "__main__":
    start_server()
