# CyberScope

CyberScope is a scalable personal project designed for learning and practicing cybersecurity. It starts with a basic **port scanner** and expands with advanced features such as **FTP honeypot**, **password manager**, and **port scanning tools**. The project allows users to interact via the terminal for a more hands-on cybersecurity experience.

## 🔥 Main Features

### 1️⃣ **Port Scanner**
- Scan a range of ports to detect open ones.
- Identify active services running on open ports.

### 2️⃣ **Honeypot (FTP Simulation)**
- Simulated FTP server that allows any user to log in without authentication.
- Supports basic FTP commands: `ls`, `get`, `put`, and `quit`.
- Files are uploaded/downloaded in the `Files/` directory.
- Logs all activities, including login attempts and file transfers.

### 3️⃣ **Password Manager**
- Stores passwords securely using encryption (Fernet from `cryptography`).
- Allows password retrieval and management.
- Generates random strong passwords.

### 4️⃣ **Activity Logging & Detection**
- Logs all relevant events (connections, disconnections, commands executed).
- Detects **suspicious behavior** such as **port scans**, **rapid connections**, and **DoS attempts**.
- Saves logs in `Logs/logs.txt`.

---

## 📌 **Supported Commands**

### **FTP**
| Command        | Description |
|---------------|-------------|
| `ls`          | List available files on the server |
| `get <file>`  | Download a file from the server (saved in `Files/`) |
| `put <file>`  | Upload a file to the server |
| `quit`        | Exit the FTP session |

### **Port Scanner**
| Command | Description |
|---------|-------------|
| `scan <IP> <port-range>` | Scans a given IP and port range for open ports |

### **Password Manager**
| Command            | Description |
|--------------------|-------------|
| `store`           | Save a new password securely |
| `retrieve <site>` | Retrieve stored credentials for a site |
| `generate`        | Generate a secure password |

---

## 🚀 **Installation & Usage**

### **1️⃣ Clone the repository**
```bash
git clone https://github.com/yourusername/CyberScope.git
cd CyberScope
```

### **2️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Start the Honeypot FTP Server**
```bash
python Server/server.py
```

### **4️⃣ Run the Client Application**
```bash
python Client/main.py
```