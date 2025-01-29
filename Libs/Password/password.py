import os
import base64
import json
from cryptography.fernet import Fernet
import secrets
import string
from colorama import Fore, Style, init
from Libs.Utils.utils import print_underline

init()

PASSWORD_FILE = "passwords.enc"
KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data).decode()

def save_passwords(passwords, key):
    encrypted_data = encrypt_data(json.dumps(passwords), key)
    with open(PASSWORD_FILE, "wb") as file:
        file.write(encrypted_data)

def load_passwords(key):
    if not os.path.exists(PASSWORD_FILE):
        return {}
    with open(PASSWORD_FILE, "rb") as file:
        encrypted_data = file.read()
    return json.loads(decrypt_data(encrypted_data, key))

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def list_passwords(passwords):
    if not passwords:
        print(Fore.LIGHTRED_EX + "There are no saved passwords.\n" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW +  "Saved Passwords:" + Style.RESET_ALL)
        for website, creds in passwords.items():
            print(f"\n\tPlace: {Fore.LIGHTMAGENTA_EX}{website}{Style.RESET_ALL} \n\t\tUser: {creds['username']} \n\t\tPassword: {creds['password']}")

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
            website = input(Fore.CYAN + "\nEnter the website name to remove your password:" + Style.RESET_ALL).strip()
            if website in passwords:
                del passwords[website]
                save_passwords(passwords, key)
                print(Fore.LIGHTGREEN_EX + f"Password removed for{website}." + Style.RESET_ALL)
            else:
                print(Fore.LIGHTRED_EX + f"No password found for {website}." + Style.RESET_ALL)
        elif choice == "5":
            print(Fore.LIGHTRED_EX + "Exiting the password manager..." + Style.RESET_ALL)
            break
        else:
            print("Invalid option, please try again.\n")
