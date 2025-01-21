import sys
import os
from colorama import Fore, Style, init
from getpass import getpass  # Importa getpass para capturar contraseñas de forma oculta

# Añade el directorio padre al PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Libs.Utils.utils import welcome_message, print_underline, print_goodbye, welcome_message_honeypot
from Libs.Scanner.scanner import scanner
from Libs.Communication.communication import connect_ftp_server
from Libs.Password.password import password_manager

init()  # Inicializa el módulo colorama

if __name__ == "__main__":
    welcome_message()

    while True:
        print_underline()
        print(Fore.YELLOW + "Select one of the following options:\n" + Style.RESET_ALL)
        print("\t1. Port Scanning")
        print("\t2. Connect to FTP Server")
        print("\t3. Password Manager")
        print("\t4. Exit")

        opcion_menu = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)

        if opcion_menu == "1":
            scanner()
        elif opcion_menu == "2":
            welcome_message_honeypot()
            host = input(Fore.YELLOW + "\nFTP Server Address: " + Style.RESET_ALL).strip()
            port = int(input(Fore.YELLOW + "FTP Port (default 21): " + Style.RESET_ALL).strip() or 21)
            username = input(Fore.YELLOW + "FTP Username: " + Style.RESET_ALL).strip()
            password = getpass(Fore.YELLOW + "FTP Password: " + Style.RESET_ALL)  # Usa getpass para la contraseña
            connect_ftp_server(host, port, username, password)
        elif opcion_menu == "3":
            password_manager()
        elif opcion_menu == "4":
            print_goodbye()
            break
        else:
            print(Fore.LIGHTRED_EX + "Invalid option. Please select 1, 2, or 3." + Style.RESET_ALL)
