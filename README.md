# CyberScope

CyberScope is a terminal-based cybersecurity toolkit written in Python, built as a personal project to learn security concepts hands-on. It bundles three tools behind a single interactive menu:

- a **TCP port scanner** that exports HTML/CSV reports
- an **FTP honeypot** that logs activity and flags floods
- an **encrypted password manager** backed by Fernet

> [!WARNING]
> This project is for learning and for use on systems you own or have written permission to test. Port scanning third-party hosts without authorization is illegal in many jurisdictions. The honeypot is a deliberately exposed service, so run it in an isolated environment (VM or container), never on a machine holding sensitive data.

---

## Features

### Port scanner

Scans a TCP port range using `connect_ex` and reports each port as open or closed. Three modes:

| Mode | Range | Timeout |
|---|---|---|
| Quick | 20-1024 | 0.3s |
| Detailed | 1-65535 | 0.7s |
| Custom | you choose | you choose |

Results can be exported as an **HTML table** or a **CSV file**, written to `logs/report_<ip>_<timestamp>.<ext>`.

> [!NOTE]
> The scanner reports reachability only. It does not fingerprint services or grab banners, so an open port tells you something is listening, not what.

### FTP honeypot

A real FTP server (built on `pyftpdlib`) that serves the `ftp_root/` directory with full read/write permissions, intended as bait to observe what an intruder does.

It logs connects, disconnects, logins, logouts, uploads, downloads and every command to `Logs/logs.txt`, and prints an alert when it detects:

- **connection floods** — more than 10 connections from one IP within 10 seconds
- **command floods** — more than 20 commands from one IP within 10 seconds

Login requires the credentials hardcoded in `Server/server.py` (`user` / `password`). Change them, and note that the honeypot does *not* accept anonymous logins.

### Password manager

Stores credentials encrypted with **Fernet** (AES-128-CBC + HMAC) from the `cryptography` library. It can save entries, list them, generate strong random passwords via `secrets`, and delete entries. Data lives in `passwords.enc`, encrypted with the key in `secret.key`.

> [!CAUTION]
> `secret.key` is the only thing protecting `passwords.enc` — anyone with both can read every stored password in plaintext. Both files are gitignored; keep it that way and never commit them. This is a learning exercise, not a substitute for an audited password manager.

---

## Requirements

- Python 3.8+
- Linux/macOS recommended (the honeypot binds port 21)

## Installation

```bash
git clone https://github.com/Armandls/CyberScope.git
cd CyberScope
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

> [!IMPORTANT]
> Both scripts resolve their data directories relative to the current working directory, so `cd` into `Server/` or `Client/` before running them. Launching from the repository root will create a stray `ftp_root/` and ignore the sample files.

### Start the honeypot

Port 21 is privileged, so binding it requires root — without `sudo` you get `PermissionError: [Errno 13]`:

```bash
cd Server
sudo ../venv/bin/python server.py
```

To avoid `sudo`, change the port in `Server/server.py` to something above 1024 (e.g. `2121`) and run it as your normal user.

### Run the client

In a second terminal:

```bash
cd Client
python main.py
```

You get a menu:

```
1. Port Scanning
2. Connect to FTP Server
3. Password Manager
4. Exit
```

Each tool then prompts for what it needs — there are no command-line arguments. Option 2 asks for host, port, username and password (entered hidden via `getpass`), then opens an FTP prompt supporting:

| Command | Description |
|---|---|
| `ls` | List files on the server |
| `get <file>` | Download a file into `Client/Files/` |
| `put <file>` | Upload a file from `Client/Files/` |
| `quit` | End the session |

---

## Project layout

```
CyberScope/
├── Client/
│   ├── main.py          # Interactive menu entry point
│   └── Files/           # Local FTP download/upload directory
├── Server/
│   ├── server.py        # FTP honeypot + flood detection
│   └── ftp_root/        # Directory exposed to FTP clients
├── Libs/
│   ├── Scanner/         # Port scanning
│   ├── Reporter/        # HTML/CSV report generation
│   ├── Communication/   # FTP client session
│   ├── Password/        # Fernet-encrypted password manager
│   └── Utils/           # Banners, logging, helpers
└── requirements.txt
```

Generated at runtime: `logs/` (scan reports), `Logs/logs.txt` (honeypot events), `passwords.enc` and `secret.key` (password manager).

## Roadmap

- Service and version detection on open ports
- Concurrent scanning to speed up full-range scans
- Configurable honeypot port and credentials via config file or CLI flags
- Master-password key derivation for the password manager
