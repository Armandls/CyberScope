import socket
from colorama import Fore, Style, init
import csv
import os
from datetime import datetime

init()  # Inicializa el módulo colorama

# Crea la carpeta "logs" si no existe
def crear_directorio_logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")
        print(Fore.CYAN + "Directorio 'logs' creado." + Style.RESET_ALL)

def escanear_puertos(ip, puerto_inicio, puerto_fin, timeout):
    print(f"\nEscaneando {ip} desde el puerto {puerto_inicio} hasta {puerto_fin}...")
    resultados = []  # Lista para almacenar los resultados del escaneo
    for puerto in range(puerto_inicio, puerto_fin + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP con IPv4
        sock.settimeout(timeout)  # Establece el tiempo de espera
        resultado = sock.connect_ex((ip, puerto))  # connect_ex devuelve 0 si el puerto está abierto
        if resultado == 0:
            print(Fore.GREEN + f"Puerto {puerto} está abierto" + Style.RESET_ALL)
            resultados.append((puerto, "Abierto"))
        else:
            resultados.append((puerto, "Cerrado"))
        sock.close()
    return resultados

# Genera un reporte en formato HTML
def generar_reporte_html(resultados, ip):
    crear_directorio_logs()
    nombre_archivo = f"logs/reporte_{ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(nombre_archivo, "w") as archivo:
        archivo.write("<html><head><title>Reporte de Escaneo de Puertos</title></head><body>")
        archivo.write(f"<h1>Reporte de Escaneo de Puertos para {ip}</h1>")
        archivo.write("<table border='1'><tr><th>Puerto</th><th>Estado</th></tr>")
        for puerto, estado in resultados:
            archivo.write(f"<tr><td>{puerto}</td><td>{estado}</td></tr>")
        archivo.write("</table></body></html>")
    print(Fore.CYAN + f"Reporte HTML generado: {nombre_archivo}" + Style.RESET_ALL)

# Genera un reporte en formato CSV
def generar_reporte_csv(resultados, ip):
    crear_directorio_logs()
    nombre_archivo = f"logs/reporte_{ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(nombre_archivo, "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Puerto", "Estado"])
        escritor.writerows(resultados)
    print(Fore.CYAN + f"Reporte CSV generado: {nombre_archivo}" + Style.RESET_ALL)

# Función para determinar el rango de puertos según el modo de escaneo
def seleccionar_modo(ip):
    print(Fore.CYAN + "\nSelecciona el modo de escaneo:" + Style.RESET_ALL)
    print("1. Escaneo rápido (puertos comunes)")
    print("2. Escaneo detallado (todos los puertos)")
    print("3. Escaneo personalizado")
    
    opcion = input(Fore.YELLOW + "Introduce tu elección (1/2/3): " + Style.RESET_ALL)
    
    if opcion == "1":
        puerto_inicio, puerto_fin, timeout = 20, 1024, 0.3
        print(Fore.CYAN + "Modo: Escaneo rápido" + Style.RESET_ALL)
    elif opcion == "2":
        puerto_inicio, puerto_fin, timeout = 1, 65535, 0.7
        print(Fore.CYAN + "Modo: Escaneo detallado" + Style.RESET_ALL)
    elif opcion == "3":
        puerto_inicio = int(input(Fore.YELLOW + "Introduce el puerto inicial: " + Style.RESET_ALL))
        puerto_fin = int(input(Fore.YELLOW + "Introduce el puerto final: " + Style.RESET_ALL))
        timeout = float(input(Fore.YELLOW + "Introduce el tiempo de espera (segundos): " + Style.RESET_ALL))
        print(Fore.CYAN + "Modo: Escaneo personalizado" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Opción no válida. Usando escaneo rápido por defecto." + Style.RESET_ALL)
        puerto_inicio, puerto_fin, timeout = 20, 1024, 0.3

    return puerto_inicio, puerto_fin, timeout

# Ejemplo de uso
if __name__ == "__main__":
    direccion_ip = input(Fore.YELLOW + "Introduce la dirección IP a escanear: " + Style.RESET_ALL)
    puerto_inicio, puerto_fin, timeout = seleccionar_modo(direccion_ip)
    resultados = escanear_puertos(direccion_ip, puerto_inicio, puerto_fin, timeout)

    print(Fore.CYAN + "\nSelecciona el formato del reporte:" + Style.RESET_ALL)
    print("1. HTML")
    print("2. CSV")
    formato = input(Fore.YELLOW + "Introduce tu elección (1/2): " + Style.RESET_ALL)

    if formato == "1":
        generar_reporte_html(resultados, direccion_ip)
    elif formato == "2":
        generar_reporte_csv(resultados, direccion_ip)
    else:
        print(Fore.RED + "Formato no válido. No se generó ningún reporte." + Style.RESET_ALL)
