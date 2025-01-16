import socket
from threading import Thread
from colorama import Fore, Style, init

init()  # Inicializa el módulo colorama

# Función para manejar a cada cliente
def handle_client(cliente_socket, direccion_cliente):
  
    try:
        while True:
            # Recibe datos del cliente
            datos = cliente_socket.recv(1024).decode()
            if not datos:
                print(Fore.RED + f"Client {direccion_cliente} disconnected unexpectedly." + Style.RESET_ALL)
                break

            print(Fore.CYAN + f"\nRequest received from {direccion_cliente}: {datos}" + Style.RESET_ALL)

            # Maneja los comandos recibidos
            if datos == "CONNECT":
                print(Fore.GREEN + "Client connected: IP " + direccion_cliente[0] + " Port " + str(direccion_cliente[1]) + Style.RESET_ALL)
                respuesta = "Connection established with the Honeypot server."
                cliente_socket.sendall(respuesta.encode())
            elif datos == "DISCONNECT":
                print(Fore.RED + f"Client requested disconnection: {direccion_cliente}" + Style.RESET_ALL)
                respuesta = "Connection closed."
                cliente_socket.sendall(respuesta.encode())
                break
            else:
                print(Fore.YELLOW + f"Unknown command from {direccion_cliente}: {datos}" + Style.RESET_ALL)
                respuesta = "Unknown command."
                cliente_socket.sendall(respuesta.encode())

    except ConnectionResetError:
        print(Fore.RED + f"Connection reset by client: {direccion_cliente}" + Style.RESET_ALL)
    finally:
        cliente_socket.close()

# Función principal para iniciar el servidor
def start_server(host="127.0.0.1", puerto=8080):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Vincula el socket a la dirección y el puerto
        servidor_socket.bind((host, puerto))
        servidor_socket.listen(5)  # Escucha conexiones entrantes
        print(Fore.YELLOW + f"\nServer started on {host}:{puerto}. Waiting for connections..." + Style.RESET_ALL)
        
        while True:
            # Acepta una nueva conexión
            cliente_socket, direccion_cliente = servidor_socket.accept()
            # Inicia un hilo para manejar al cliente
            cliente_thread = Thread(target=handle_client, args=(cliente_socket, direccion_cliente))
            cliente_thread.start()
    
    except KeyboardInterrupt:
        # Maneja Ctrl+C para salir limpiamente
        print(Fore.RED + "\nServer stopped by user. Exiting..." + Style.RESET_ALL)
    finally:
        servidor_socket.close()
        print(Fore.YELLOW + "Server socket closed. Goodbye!" + Style.RESET_ALL)

# Inicia el servidor
if __name__ == "__main__":
    start_server()
