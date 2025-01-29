import socket
from colorama import Fore, Style
from Libs.Reporter.reporter import generate_report_html, generate_report_csv
from Libs.Utils.utils import print_underline

def scan_ports(ip, puerto_inicio, puerto_fin, timeout):
    print(f"\nScanning {ip} from port {puerto_inicio} to {puerto_fin}...")
    resultados = []  # Lista para almacenar los resultados del escaneo
    for puerto in range(puerto_inicio, puerto_fin + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP con IPv4
        sock.settimeout(timeout)  # Establece el tiempo de espera
        resultado = sock.connect_ex((ip, puerto))  # connect_ex devuelve 0 si el puerto está abierto
        if resultado == 0:
            print(Fore.GREEN + f"Port {puerto} is open" + Style.RESET_ALL)
            resultados.append((puerto, "Open"))
        else:
            resultados.append((puerto, "Close"))
        sock.close()
    return resultados

def select_mode():
    print(Fore.YELLOW + "\nSelect scan mode:" + Style.RESET_ALL)
    print("\t1. Quick scan (common ports)")
    print("\t2. Detailed scan (all ports)")
    print("\t3. Custom scan")
    
    opcion = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)
    if opcion == "1":
        return 20, 1024, 0.3
    elif opcion == "2":
        return 1, 65535, 0.7
    elif opcion == "3":
        puerto_inicio = int(input(Fore.YELLOW + "\nEnter the initial port: " + Style.RESET_ALL))
        puerto_fin = int(input(Fore.YELLOW + "Enter the final port: " + Style.RESET_ALL))
        timeout = float(input(Fore.YELLOW + "Enter the wait time (seconds): " + Style.RESET_ALL))
        return puerto_inicio, puerto_fin, timeout
    else:
        print(Fore.RED + "Invalid option. Using quick scan by default." + Style.RESET_ALL)
        return 20, 1024, 0.3

def scanner():

    print_underline()

    direccion_ip = input(Fore.YELLOW + "Enter the IP address to scan: " + Style.RESET_ALL)
    puerto_inicio, puerto_fin, timeout = select_mode()
    resultados = scan_ports(direccion_ip, puerto_inicio, puerto_fin, timeout)

    print(Fore.YELLOW + "\nSelect the report format:" + Style.RESET_ALL)
    print("\t1. HTML")
    print("\t2. CSV")
    print("\t3. No report")
    formato = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)

    if formato == "1":
        generate_report_html(resultados, direccion_ip)
    elif formato == "2":
        generate_report_csv(resultados, direccion_ip)
    elif formato == "3":
        pass
    else:
        print(Fore.RED + "Invalid format. No report was generated." + Style.RESET_ALL)

    print(Fore.GREEN + "Scan finished!" + Style.RESET_ALL)
