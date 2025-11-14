# 🔎 Advanced Port Scanner (Python)

A fast, multi-threaded **TCP port scanning tool** built for reconnaissance, network enumeration, and OSCP-style labs.
This scanner supports **custom port ranges**, **banner grabbing**, **randomized scan order (IDS evasion)**, and **JSON/TXT reporting**.

This version replaces the simplistic beginner script with a **professional-grade scanning utility** suitable for security portfolios and real-world assessments.

---

<p align="center">
  <img src="assets/Port Scanner.png" width="600">
</p>
<br>
<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen">
  <img src="https://img.shields.io/badge/language-python-blue">
  <img src="https://img.shields.io/badge/type-offensive%20security-red">
  <img src="https://img.shields.io/badge/license-MIT-yellow">
</p>

# 📂 Project Structure

```
basic-port-scanner/
│── src/
│   └── port_scanner.py
│── reports/
│   └── .gitkeep
│── wordlists/
│   └── .gitkeep
│── README.md
│── LICENSE
```

---

# 🚀 Features

### ✔ Multi-threaded TCP Connect Scanning

Uses **100 concurrent threads** to accelerate scanning, handling large port ranges efficiently.

### ✔ Customizable Port Inputs

Supports:

```
-p 1-1024           # range
-p 80,443,3306      # comma-separated
-p 22               # single port
```

### ✔ Banner Grabbing

Identifies running services by capturing application banners:

```
SSH-2.0-OpenSSH_8.2
Apache/2.4.54
MySQL Protocol 10
```

### ✔ Randomized Port Order (Basic IDS Evasion)

Ports are shuffled before scanning to avoid linear port sweep signatures.

### ✔ JSON & TXT Reporting

Reports stored under `/reports/`:

* JSON structured report
* TXT list of open ports

### ✔ Graceful Error Handling

Handles:

* Host resolution errors
* Network timeouts
* Connection failures
* Interrupted scans

---

# 🧪 Usage

### **Scan common port range (1–1024)**

```bash
python3 src/port_scanner.py 192.168.1.10 -p 1-1024
```

### **Scan a custom set of ports**

```bash
python3 src/port_scanner.py scanme.nmap.org -p 80,443,22,3306
```

### **Scan a single port**

```bash
python3 src/port_scanner.py example.com -p 443
```

### Example Output

```
========== Port Scan Started ==========
Target: 192.168.1.10
Ports: 1-1024
Threads: 100
----------------------------------------

[OPEN] 22/tcp  →  SSH-2.0-OpenSSH_8.2
[OPEN] 80/tcp

========== Scan Complete ==========
Open Ports Found: 2
Scan Duration: 3.24 seconds
====================================
```

---

# 📄 Generated Reports

Inside `/reports/`:

```
portscan-20251114-160420.json
portscan-20251114-160420.txt
```

### JSON Example

```json
{
  "target": "192.168.1.10",
  "open_ports": [
    {"port": 22, "banner": "SSH-2.0-OpenSSH_8.2"},
    {"port": 80, "banner": null}
  ],
  "scan_duration": 3.24
}
```

---

# 🛠 How It Works (Internals)

### 1. Host Resolution

Resolves domain → IPv4:

```
socket.gethostbyname(target)
```

### 2. Multi-threaded Connect Scan

Each worker pulls a port from a queue and attempts:

```
s.connect_ex((ip, port))
```

If result == 0 → port open.

### 3. Banner Grabbing

If port is open, tool attempts:

```
s.recv(1024)
```

to capture service fingerprints.

### 4. Randomized Port Order

Shuffles ports for basic stealth against sequential-scan detection.

### 5. Reporting

Results compiled into:

* TXT output
* JSON structured file

---

# 📈 Performance

Testing on local VM:

| Ports Scanned | Threads | Duration |
| ------------- | ------- | -------- |
| 1–1024        | 100     | ~3s      |
| 1–65535       | 300     | ~40–60s  |

(Depends heavily on latency and host responsiveness.)

---

# 📌 Future Enhancements

* Asyncio-based ultra-fast scanning
* SYN-scan mode (requires raw sockets)
* UDP scanning mode
* OS fingerprinting (TTL analysis)
* NSE-style script hooks
* Banner signature matching

---

# 🧑‍⚖️ Ethical Disclaimer

This tool is intended **ONLY** for:

* Authorized penetration testing
* Lab environments
* Educational use

Scanning systems you do not own or have permission to test is **illegal and unethical**.

---

# 👨‍💻 Author

**Vignesh Mani**
Offensive Security Researcher
GitHub: [https://github.com/vigneshoffsec](https://github.com/vigneshoffsec)
LinkedIn: [https://linkedin.com/in/vignesh-m17](https://linkedin.com/in/vignesh-m17)
