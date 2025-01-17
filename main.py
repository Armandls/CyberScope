from colorama import Fore, Style, init
from utils.utils import welcome_message, print_underline
from scanner.scanner import scanner
from honeypot.honeypot import connect_honeypot


init()  # Inicializa el módulo colorama

if __name__ == "__main__":
    welcome_message()

    while True:
        print(Fore.YELLOW + "Select one of the following options:\n" + Style.RESET_ALL)
        print("\t1. Port Scanning")
        print("\t2. Connect to Honeypot")
        print("\t3. Exit")

        opcion_menu = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)

        if opcion_menu == "1":
            print_underline()
            scanner()
            print_underline()
        elif opcion_menu == "2":
            print_underline()
            connect_honeypot()
            print_underline()
        elif opcion_menu == "3":
            print(Fore.BLUE + "\nBye Bye... Good night my little baby🥶\n" + Style.RESET_ALL)
            exit()
        else:
            print(Fore.RED + "Opción no válida. Por favor, selecciona 1 o 2." + Style.RESET_ALL)
