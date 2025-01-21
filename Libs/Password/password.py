import os
import base64
import json
from cryptography.fernet import Fernet
import secrets
import string
from colorama import Fore, Style, init
from Libs.Utils.utils import print_underline

init()

# Archivo de almacenamiento cifrado
PASSWORD_FILE = "passwords.enc"
KEY_FILE = "secret.key"

# Generar clave de cifrado
def generate_key():
    """Genera una clave y la guarda en un archivo."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

# Cargar clave existente
def load_key():
    """Carga la clave desde el archivo."""
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Encriptar datos
def encrypt_data(data, key):
    """Cifra los datos usando la clave proporcionada."""
    f = Fernet(key)
    return f.encrypt(data.encode())

# Desencriptar datos
def decrypt_data(data, key):
    """Descifra los datos usando la clave proporcionada."""
    f = Fernet(key)
    return f.decrypt(data).decode()

# Guardar contraseñas en el archivo cifrado
def save_passwords(passwords, key):
    """Guarda el diccionario de contraseñas cifrado."""
    encrypted_data = encrypt_data(json.dumps(passwords), key)
    with open(PASSWORD_FILE, "wb") as file:
        file.write(encrypted_data)

# Cargar contraseñas del archivo cifrado
def load_passwords(key):
    """Carga y descifra el diccionario de contraseñas."""
    if not os.path.exists(PASSWORD_FILE):
        return {}
    with open(PASSWORD_FILE, "rb") as file:
        encrypted_data = file.read()
    return json.loads(decrypt_data(encrypted_data, key))

# Generar contraseña aleatoria
def generate_random_password(length=12):
    """Genera una contraseña aleatoria."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def list_passwords(passwords):
    if not passwords:
        print(Fore.LIGHTRED_EX + "There are no saved passwords.\n" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW +  "Saved Passwords:" + Style.RESET_ALL)
        for website, creds in passwords.items():
            print(f"\n\tPlace: {Fore.LIGHTMAGENTA_EX}{website}{Style.RESET_ALL} \n\t\tUser: {creds['username']} \n\t\tPassword: {creds['password']}")

# Menú principal
def password_manager():
    key = load_key()
    passwords = load_passwords(key)

    while True:
        print_underline()
        print(Fore.YELLOW + "Password Manager\n" + Style.RESET_ALL)
        print("\t1. Save a new password")
        print("\t2. View saved passwords")
        print("\t3. Generate a random password")
        print("\t4. Delete a password")
        print("\t5. Exit")

        choice = input(Fore.CYAN + "\nSelect an option (1/2/3/4): " + Style.RESET_ALL).strip()
        if choice == "1":
            print_underline()
            website = input(Fore.YELLOW + "Enter the website name: " + Style.RESET_ALL).strip()
            username = input(Fore.YELLOW +  "Enter the username: " + Style.RESET_ALL).strip()
            password = input(Fore.YELLOW + "Enter the password: " + Style.RESET_ALL).strip()
            passwords[website] = {"username": username, "password": password}
            save_passwords(passwords, key)
            print(Fore.LIGHTGREEN_EX + f"\nPassword saved for {website}." + Style.RESET_ALL)
        elif choice == "2":
            print_underline()
            list_passwords(passwords)
        elif choice == "3":
            print_underline()
            length = int(input(Fore.YELLOW + "Password length (default 12): " + Style.RESET_ALL) or 12)
            random_password = generate_random_password(length)
            print(f"\nGenerated password: {random_password}")
        elif choice == "4":
            print_underline()
            list_passwords(passwords)
            website = input(Fore.CYAN + "\nIntroduce el nombre del sitio web para eliminar su contraseña: " + Style.RESET_ALL).strip()
            if website in passwords:
                del passwords[website]
                save_passwords(passwords, key)
                print(Fore.LIGHTGREEN_EX + f"Contraseña eliminada para {website}." + Style.RESET_ALL)
            else:
                print(Fore.LIGHTRED_EX + f"No se encontró ninguna contraseña para {website}." + Style.RESET_ALL)
        elif choice == "5":
            print(Fore.LIGHTRED_EX + "Exiting the password manager..." + Style.RESET_ALL)
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.\n")
