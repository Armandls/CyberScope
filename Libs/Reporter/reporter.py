import csv
from datetime import datetime
from colorama import Fore, Style
from Libs.Utils.utils import create_log_directory

def generate_report_html(results, ip):
    create_log_directory()
    filename = f"logs/report_{ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w") as file:
        file.write("<html><head><title>Port Scan Report</title></head><body>")
        file.write(f"<h1>Port Scan Report for {ip}</h1>")
        file.write("<table border='1'><tr><th>Port</th><th>Status</th></tr>")
        for port, status in results:
            file.write(f"<tr><td>{port}</td><td>{status}</td></tr>")
        file.write("</table></body></html>")
    print(Fore.CYAN + f"HTML report generated: {filename}" + Style.RESET_ALL)

def generate_report_csv(results, ip):
    create_log_directory()
    filename = f"logs/report_{ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Status"])
        writer.writerows(results)
    print(Fore.CYAN + f"CSV report generated: {filename}" + Style.RESET_ALL)
