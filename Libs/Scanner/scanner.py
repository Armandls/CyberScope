import socket
from colorama import Fore, Style
from Libs.Reporter.reporter import generate_report_html, generate_report_csv
from Libs.Utils.utils import print_underline

def scan_ports(ip, start_port, end_port, timeout):
    print(f"\nScanning {ip} from port {start_port} to {end_port}...")
    results = []  # List that stores the scan results
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket over IPv4
        sock.settimeout(timeout)  # Set the timeout
        result = sock.connect_ex((ip, port))  # connect_ex returns 0 if the port is open
        if result == 0:
            print(Fore.GREEN + f"Port {port} is open" + Style.RESET_ALL)
            results.append((port, "Open"))
        else:
            results.append((port, "Closed"))
        sock.close()
    return results

def select_mode():
    print(Fore.YELLOW + "\nSelect scan mode:" + Style.RESET_ALL)
    print("\t1. Quick scan (common ports)")
    print("\t2. Detailed scan (all ports)")
    print("\t3. Custom scan")
    
    choice = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)
    if choice == "1":
        return 20, 1024, 0.3
    elif choice == "2":
        return 1, 65535, 0.7
    elif choice == "3":
        start_port = int(input(Fore.YELLOW + "\nEnter the initial port: " + Style.RESET_ALL))
        end_port = int(input(Fore.YELLOW + "Enter the final port: " + Style.RESET_ALL))
        timeout = float(input(Fore.YELLOW + "Enter the wait time (seconds): " + Style.RESET_ALL))
        return start_port, end_port, timeout
    else:
        print(Fore.RED + "Invalid option. Using quick scan by default." + Style.RESET_ALL)
        return 20, 1024, 0.3

def scanner():

    print_underline()

    ip_address = input(Fore.YELLOW + "Enter the IP address to scan: " + Style.RESET_ALL)
    start_port, end_port, timeout = select_mode()
    results = scan_ports(ip_address, start_port, end_port, timeout)

    print(Fore.YELLOW + "\nSelect the report format:" + Style.RESET_ALL)
    print("\t1. HTML")
    print("\t2. CSV")
    print("\t3. No report")
    report_format = input(Fore.CYAN + "\nEnter your choice (1/2/3): " + Style.RESET_ALL)

    if report_format == "1":
        generate_report_html(results, ip_address)
    elif report_format == "2":
        generate_report_csv(results, ip_address)
    elif report_format == "3":
        pass
    else:
        print(Fore.RED + "Invalid format. No report was generated." + Style.RESET_ALL)

    print(Fore.GREEN + "Scan finished!" + Style.RESET_ALL)
