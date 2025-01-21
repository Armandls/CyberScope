import socket
import threading
from colorama import Fore, Style, init
from datetime import datetime
import os
from collections import defaultdict
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

init()  # Inicializa colorama

# Constantes para la detección de comportamiento sospechoso
MAX_CONNECTIONS = 10  # Máximo de conexiones permitidas por IP en un intervalo
CONNECTION_TIME_WINDOW = 10  # Intervalo de tiempo en segundos
COMMAND_THRESHOLD = 20  # Número máximo de comandos en un tiempo corto
COMMAND_TIME_WINDOW = 10  # Ventana de tiempo para detección de comandos rápidos

# Variables globales para rastrear actividad
ip_connections = defaultdict(list)  # Registra conexiones por IP
command_activity = defaultdict(list)  # Registra comandos por IP

# Función para escribir en el log
def write_log(event_type, message):
    os.makedirs("Logs", exist_ok=True)  # Crea la carpeta si no existe
    with open("Logs/logs.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] EVENT: {event_type} - {message}\n")

# Detección de actividad sospechosa
def is_suspicious(ip, activity_log, threshold, time_window):
    """Detecta comportamiento sospechoso basado en actividad reciente."""
    now = datetime.now()
    activity_log[ip] = [t for t in activity_log[ip] if (now - t).seconds <= time_window]
    activity_log[ip].append(now)

    return len(activity_log[ip]) > threshold

# Clase personalizada para manejar eventos del servidor FTP
class CustomFTPHandler(FTPHandler):
    def on_connect(self):
        """Se llama cuando un cliente se conecta al servidor."""
        client_info = f"{self.remote_ip}:{self.remote_port}"
        write_log("CONNECT", f"Client connected: {client_info}")

        # Detecta conexiones rápidas desde una IP
        if is_suspicious(self.remote_ip, ip_connections, MAX_CONNECTIONS, CONNECTION_TIME_WINDOW):
            write_log("ALERT", f"Suspicious activity detected: Too many connections from {self.remote_ip}")
            print(Fore.RED + f"Suspicious activity detected: Too many connections from {self.remote_ip}" + Style.RESET_ALL)

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

    def on_file_received(self, file):
        """Se llama cuando un archivo es recibido con éxito."""
        write_log("UPLOAD", f"File uploaded: {file}")

    def on_file_sent(self, file):
        """Se llama cuando un archivo es enviado con éxito."""
        write_log("DOWNLOAD", f"File downloaded: {file}")

    def on_command(self, command, args):
        """Se llama en cada comando recibido del cliente."""
        write_log("COMMAND", f"Command received: {command} {args}")

        # Detecta comandos repetitivos en un intervalo corto
        if is_suspicious(self.remote_ip, command_activity, COMMAND_THRESHOLD, COMMAND_TIME_WINDOW):
            write_log("ALERT", f"Suspicious activity detected: Command flood from {self.remote_ip}")
            print(Fore.RED + f"Suspicious activity detected: Command flood from {self.remote_ip}" + Style.RESET_ALL)

# Configuración del servidor FTP
def start_ftp_server():
    authorizer = DummyAuthorizer()
    ftp_root = "ftp_root"  # Directorio raíz del servidor FTP
    os.makedirs(ftp_root, exist_ok=True)  # Crea el directorio si no existe
    authorizer.add_user("user", "password", ftp_root, perm="elradfmw")  # Usuario FTP

    handler = CustomFTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer(("0.0.0.0", 21), handler)
    print(Fore.YELLOW + "FTP server is running on port 21." + Style.RESET_ALL)
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
