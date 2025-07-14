import socket
from datetime import datetime

# Target to scan
target = input("Enter target IP or domain: ")

# Banner
print("-" * 50)
print(f"Scanning Target: {target}")
print("Scanning started at: " + str(datetime.now()))
print("-" * 50)

try:
    for port in range(1, 1025):  # You can change the port range
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        s.close()

except KeyboardInterrupt:
    print("\nExiting Program.")
except socket.gaierror:
    print("\nHostname Could Not Be Resolved.")
except socket.error:
    print("\nServer not responding.")

