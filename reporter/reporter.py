import os
import csv
from datetime import datetime
from colorama import Fore, Style
from utils.utils import create_log_directory

def generate_report_html(resultados, ip):
    create_log_directory()
    nombre_archivo = f"logs/reporte_{ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(nombre_archivo, "w") as archivo:
        archivo.write("<html><head><title>Reporte de Escaneo de Puertos</title></head><body>")
        archivo.write(f"<h1>Reporte de Escaneo de Puertos para {ip}</h1>")
        archivo.write("<table border='1'><tr><th>Puerto</th><th>Estado</th></tr>")
        for puerto, estado in resultados:
            archivo.write(f"<tr><td>{puerto}</td><td>{estado}</td></tr>")
        archivo.write("</table></body></html>")
    print(Fore.CYAN + f"HTML report generated: {nombre_archivo}" + Style.RESET_ALL)

def generate_report_csv(resultados, ip):
    crear_directorio_logs()
    nombre_archivo = f"logs/reporte_{ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(nombre_archivo, "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Puerto", "Estado"])
        escritor.writerows(resultados)
    print(Fore.CYAN + f"CSV report generated: {nombre_archivo}" + Style.RESET_ALL)
