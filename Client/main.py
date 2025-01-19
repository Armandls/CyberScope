import sys
import os
from colorama import Fore, Style, init
from getpass import getpass  # Importa getpass para capturar contraseñas de forma oculta

# Añade el directorio padre al PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Libs.Utils.utils import welcome_message, print_underline, welcome_message_honeypot, print_incorrect, print_goodbye
from Libs.Scanner.scanner import scanner
from Libs.Communication.communication import connect_ftp_server, connect_ssh_server

init()  # Inicializa el módulo colorama

def connect_honeypot():

    welcome_message_honeypot()

    while True:
        print_underline()
        print(Fore.YELLOW + "\nSelect one of the following services:\n" + Style.RESET_ALL)
        print("\t1. Connect to FTP")
        print("\t2. Connect to SSH")
        print("\t3. Exit")

        choice = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL).strip()

        if choice == "1":
            print_underline()
            host = input(Fore.YELLOW + "\nFTP Server Address: " + Style.RESET_ALL).strip()
            port = int(input(Fore.YELLOW + "FTP Port (default 21): " + Style.RESET_ALL).strip() or 21)
            username = input(Fore.YELLOW + "FTP Username: " + Style.RESET_ALL).strip()
            password = getpass(Fore.YELLOW + "FTP Password: " + Style.RESET_ALL)  # Usa getpass para la contraseña
            connect_ftp_server(host, port, username, password)
        elif choice == "2":
            print_underline()
            host = input(Fore.YELLOW + "\nSSH Server Address: " + Style.RESET_ALL).strip()
            port = int(input(Fore.YELLOW + "SSH Port (default 22): " + Style.RESET_ALL).strip() or 22)
            username = input(Fore.YELLOW + "SSH Username: " + Style.RESET_ALL).strip()
            password = getpass(Fore.YELLOW + "SSH Password: " + Style.RESET_ALL)  # Usa getpass para la contraseña
            connect_ssh_server(host, port, username, password)
        elif choice == "3":
            print_incorrect()
        elif choice == "666":
            print_goodbye()
            return
        else:
            print_incorrect()

if __name__ == "__main__":
    welcome_message()

    while True:
        print_underline()
        print(Fore.YELLOW + "Select one of the following options:\n" + Style.RESET_ALL)
        print("\t1. Port Scanning")
        print("\t2. Connect to Honeypot")
        print("\t3. Exit")

        opcion_menu = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)

        if opcion_menu == "1":
            scanner()
        elif opcion_menu == "2":
            connect_honeypot()
        elif opcion_menu == "3":
            print(Fore.BLUE + "\nGoodbye! See you next time! 🥶\n" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid option. Please select 1, 2, or 3." + Style.RESET_ALL)
