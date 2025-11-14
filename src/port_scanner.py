import socket
import threading
import argparse
import time
import json
import random
from datetime import datetime
from queue import Queue
import os

# Thread settings
THREADS = 100
q = Queue()
open_ports = []

# ----- Banner Grabbing -----
def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None

# ----- Worker Function -----
def scan_port(ip):
    while not q.empty():
        port = q.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            result = s.connect_ex((ip, port))
            if result == 0:
                banner = grab_banner(ip, port)
                open_ports.append({
                    "port": port,
                    "banner": banner
                })
                if banner:
                    print(f"\033[92m[OPEN] {port}/tcp  →  {banner}\033[0m")
                else:
                    print(f"\033[92m[OPEN] {port}/tcp\033[0m")
            s.close()

        except:
            pass

        q.task_done()

# ----- Main Scanner -----
def scan(ip, ports):
    print("\n========== Port Scan Started ==========")
    print(f"Target: {ip}")
    print("Start Time:", datetime.now())
    print("Ports:", f"{min(ports)}-{max(ports)}")
    print("Threads:", THREADS)
    print("----------------------------------------\n")

    start = time.time()

    # Randomize port order for basic IDS evasion
    random.shuffle(ports)

    for port in ports:
        q.put(port)

    for _ in range(THREADS):
        t = threading.Thread(target=scan_port, args=(ip,))
        t.daemon = True
        t.start()

    q.join()

    duration = round(time.time() - start, 2)

    print("\n========== Scan Complete ==========")
    print(f"Open Ports Found: {len(open_ports)}")
    print(f"Scan Duration: {duration} seconds")
    print("====================================\n")

    return open_ports, duration

# ----- Save Reports -----
def save_reports(ip, open_ports, duration):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    os.makedirs("reports", exist_ok=True)

    # JSON
    with open(f"reports/portscan-{timestamp}.json", "w") as jf:
        json.dump({
            "target": ip,
            "open_ports": open_ports,
            "scan_duration": duration
        }, jf, indent=4)

    # TXT
    with open(f"reports/portscan-{timestamp}.txt", "w") as tf:
        for entry in open_ports:
            tf.write(f"{entry['port']} - {entry['banner']}\n")

    print(f"Reports saved inside /reports folder.\n")

# ----- Entry Point -----
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Multi-threaded Port Scanner")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument(
        "-p", "--ports",
        help="Port range (e.g. 1-1024 or 80,443,3306)",
        default="1-1024"
    )

    args = parser.parse_args()

    # Resolve host
    try:
        ip = socket.gethostbyname(args.target)
    except:
        print("\033[91m[ERROR] Unable to resolve host.\033[0m")
        exit()

    # Parse ports
    ports = []
    if "-" in args.ports:
        start, end = args.ports.split("-")
        ports = list(range(int(start), int(end) + 1))
    elif "," in args.ports:
        ports = [int(p) for p in args.ports.split(",")]
    else:
        ports = [int(args.ports)]

    open_ports, duration = scan(ip, ports)
    save_reports(ip, open_ports, duration)
