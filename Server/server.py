import socket
import threading
from colorama import Fore, Style, init
from datetime import datetime
import os
from collections import defaultdict
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

init() 

MAX_CONNECTIONS = 10  
CONNECTION_TIME_WINDOW = 10 
COMMAND_THRESHOLD = 20  
COMMAND_TIME_WINDOW = 10  

ip_connections = defaultdict(list)  
command_activity = defaultdict(list) 

def write_log(event_type, message):
    os.makedirs("Logs", exist_ok=True) 
    with open("Logs/logs.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] EVENT: {event_type} - {message}\n")

def is_suspicious(ip, activity_log, threshold, time_window):
    """Detect suspicious behavior based on recent activity."""
    now = datetime.now()
    activity_log[ip] = [t for t in activity_log[ip] if (now - t).seconds <= time_window]
    activity_log[ip].append(now)

    return len(activity_log[ip]) > threshold

class CustomFTPHandler(FTPHandler):
    def on_connect(self):
        """Called when a client connects to the server."""
        client_info = f"{self.remote_ip}:{self.remote_port}"
        write_log("CONNECT", f"Client connected: {client_info}")

        if is_suspicious(self.remote_ip, ip_connections, MAX_CONNECTIONS, CONNECTION_TIME_WINDOW):
            write_log("ALERT", f"Suspicious activity detected: Too many connections from {self.remote_ip}")
            print(Fore.RED + f"Suspicious activity detected: Too many connections from {self.remote_ip}" + Style.RESET_ALL)

    def on_disconnect(self):
        """Called when a client disconnects from the server."""
        client_info = f"{self.remote_ip}:{self.remote_port}"
        write_log("DISCONNECT", f"Client disconnected: {client_info}")

    def on_login(self, username):
        """Called when a user logs in successfully."""
        write_log("LOGIN", f"User logged in: {username}")

    def on_logout(self, username):
        """Called when a user logs out."""
        write_log("LOGOUT", f"User logged out: {username}")

    def on_file_received(self, file):
        """Called when a file is received successfully."""
        write_log("UPLOAD", f"File uploaded: {file}")

    def on_file_sent(self, file):
        """Called when a file is sent successfully."""
        write_log("DOWNLOAD", f"File downloaded: {file}")

    def on_command(self, command, args):
        """Called on every command received from the client."""
        write_log("COMMAND", f"Command received: {command} {args}")

        if is_suspicious(self.remote_ip, command_activity, COMMAND_THRESHOLD, COMMAND_TIME_WINDOW):
            write_log("ALERT", f"Suspicious activity detected: Command flood from {self.remote_ip}")
            print(Fore.RED + f"Suspicious activity detected: Command flood from {self.remote_ip}" + Style.RESET_ALL)

def start_ftp_server():
    authorizer = DummyAuthorizer()
    ftp_root = "ftp_root"  
    os.makedirs(ftp_root, exist_ok=True) 
    authorizer.add_user("user", "password", ftp_root, perm="elradfmw")  

    handler = CustomFTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer(("0.0.0.0", 21), handler)
    print(Fore.YELLOW + "FTP server is running on port 21." + Style.RESET_ALL)
    write_log("SERVICE", "FTP server started on port 21.")
    ftp_server.serve_forever()

def start_server():
    ftp_thread = threading.Thread(target=start_ftp_server, daemon=True)
    ftp_thread.start()

    try:
        ftp_thread.join()
    except KeyboardInterrupt:
        print(Fore.RED + "Stopping FTP server..." + Style.RESET_ALL)

if __name__ == "__main__":
    start_server()
