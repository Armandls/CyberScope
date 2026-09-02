import os
from colorama import Fore, Style
from datetime import datetime


def welcome_message():
        print(""" ▄████▓██   ██▓▄▄▄▄  ▓█████ ██▀███   ██████ ▄████▄  ▒█████  ██▓███ ▓█████ 
▒██▀ ▀█▒██  ██▓█████▄▓█   ▀▓██ ▒ ██▒██    ▒▒██▀ ▀█ ▒██▒  ██▓██░  ██▓█   ▀ 
▒▓█    ▄▒██ ██▒██▒ ▄█▒███  ▓██ ░▄█ ░ ▓██▄  ▒▓█    ▄▒██░  ██▓██░ ██▓▒███   
▒▓▓▄ ▄██░ ▐██▓▒██░█▀ ▒▓█  ▄▒██▀▀█▄   ▒   ██▒▓▓▄ ▄██▒██   ██▒██▄█▓▒ ▒▓█  ▄ 
▒ ▓███▀ ░ ██▒▓░▓█  ▀█░▒████░██▓ ▒██▒██████▒▒ ▓███▀ ░ ████▓▒▒██▒ ░  ░▒████▒
░ ░▒ ▒  ░██▒▒▒░▒▓███▀░░ ▒░ ░ ▒▓ ░▒▓▒ ▒▓▒ ▒ ░ ░▒ ▒  ░ ▒░▒░▒░▒▓▒░ ░  ░░ ▒░ ░
  ░  ▒ ▓██ ░▒░▒░▒   ░ ░ ░  ░ ░▒ ░ ▒░ ░▒  ░ ░ ░  ▒    ░ ▒ ▒░░▒ ░     ░ ░  ░
░      ▒ ▒ ░░  ░    ░   ░    ░░   ░░  ░  ░ ░       ░ ░ ░ ▒ ░░         ░   
░ ░    ░ ░     ░        ░  ░  ░          ░ ░ ░         ░ ░            ░  ░
░      ░ ░          ░                      ░                              
\n\n""")
        
def welcome_message_honeypot():
    print_underline()
    print(Fore.RED + """                 (       ) (       )         
 (  (      (     )\ ) ( /( )\ ) ( /( (       
 )\))(   ' )\   (()/( )\()(()/( )\()))\ )    
((_)()\ ((((_)(  /(_)((_)\ /(_)((_)\(()/(    
_(())\_)()\ _ )\(_))  _((_(_))  _((_)/(_))_  
\ \((_)/ (_)_\(_| _ \| \| |_ _|| \| (_)) __| 
 \ \/\/ / / _ \ |   /| .` || | | .` | | (_ | 
  \_/\_/ /_/ \_\|_|_\|_|\_|___||_|\_|  \___| 
                                             """)
    
    print(Fore.LIGHTRED_EX + """
This server is under active monitoring.
Your IP address and activity have been logged.
Any unauthorized attempt will be reported.
Think carefully about your next move...⌛""" + Style.RESET_ALL)
    
  
def print_goodbye():
    print_underline()
    print(Fore.RED + "  👋 Goodbye! Thanks for using CyberScope!" + Style.RESET_ALL)
    print(Fore.YELLOW + "  Remember: Security first, always! 🛡️" + Style.RESET_ALL)
    print(Fore.BLUE + "  Follow best practices and stay updated! 🚀" + Style.RESET_ALL)
    print_underline()



def create_log_directory():
    if not os.path.exists("logs"):
        os.makedirs("logs")
        print(Fore.CYAN + "'logs' directory created." + Style.RESET_ALL)

def print_underline():
    print(Fore.YELLOW + "\n---------------------------------------------------------------------" + Style.RESET_ALL)

# Function to write to the log file
def write_log(event_type, message):
    os.makedirs("Logs", exist_ok=True)  # Create the folder if it does not exist
    with open("Logs/logs.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] EVENT: {event_type} - {message}\n")


