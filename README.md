# CyberScope

CyberScope es un proyecto personal escalable diseñado para aprender y practicar ciberseguridad. Comienza con un escáner de puertos básico y se expande con funciones avanzadas como generación de informes, detección de servicios y una interfaz gráfica. Ideal para explorar herramientas y conceptos clave de manera progresiva.

## Funcionalidades principales

### 1. Escáner de Puertos
- Escaneo básico para identificar puertos abiertos en un rango especificado.
- Detección de servicios asociados a puertos abiertos.

### 2. Honeypot con soporte para FTP y SSH
- **FTP:** Simulación de un servidor FTP con comandos básicos como `ls`, `get`, `put`, y `quit`. Los archivos se suben y descargan desde la carpeta `Files`.
- **SSH:** Simulación de un servidor SSH que permite ejecutar comandos básicos como `ls`, `pwd`, y más.

### 3. Generación de Logs
- Todos los eventos importantes, como conexiones, desconexiones y comandos ejecutados, se registran en el archivo `Logs/logs.txt`.

---

## Estructura del Proyecto

CyberScope/ ├── Client/ │ ├── main.py # Cliente para interactuar con el honeypot. │ ├── Libs/ │ │ ├── Communication/ │ │ │ └── communication.py # Manejo de conexiones SSH y FTP. │ │ ├── Scanner/ │ │ │ └── scanner.py # Escáner de puertos. │ │ ├── Utils/ │ │ └── utils.py # Funciones auxiliares. ├── Server/ │ └── server.py # Honeypot con soporte para FTP y SSH. ├── Logs/ │ └── logs.txt # Archivo de registro de eventos. └── Files/ # Carpeta donde se suben y descargan archivos (FTP).

---

## Comandos Soportados

### FTP
1. **ls**: Listar los archivos disponibles en el servidor.
2. **get `<archivo>`**: Descargar un archivo del servidor al cliente (guardado en la carpeta `Files`).
3. **put `<archivo>`**: Subir un archivo desde el cliente al servidor (guardado en la carpeta `Files`).
4. **quit**: Salir de la sesión FTP.

### SSH
1. **ls**: Listar los archivos disponibles en el servidor.
2. **pwd**: Mostrar el directorio actual.
3. **exit**: Salir de la sesión SSH.
4. Otros comandos del sistema se ejecutan en el servidor.

---

## Instalación y Uso

1. Clona el repositorio:
   ```bash
   git clone https://github.com/usuario/CyberScope.git
   cd CyberScope

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

3. Inicia el servidor:
    ```bash
    python Server/server.py

4. Ejecuta el cliente:
    ```bash
    python Client/main.py
