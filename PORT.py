import socket
import threading
import time
from colorama import init
from termcolor import colored

# ==========================================
# INIT
# ==========================================

init()

# ==========================================
# BANNER
# ==========================================

print(colored("""

██████╗  ██████╗ ██████╗ ████████╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
██████╔╝██║   ██║██████╔╝   ██║
██╔═══╝ ██║   ██║██╔══██╗   ██║
██║     ╚██████╔╝██║  ██║   ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝

      REAL TIME PORT DETECTOR
      Developed By Davinder Singh

================================================
""", "cyan"))

# ==========================================
# COMMON PORTS
# ==========================================

common_ports = {

    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NETBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MYSQL",
    3389: "RDP",
    8080: "HTTP-ALT"

}

open_ports = []

# ==========================================
# SCAN FUNCTION
# ==========================================

def scan_port(target, port):

    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(1)

        result = sock.connect_ex((target, port))

        if result == 0:

            service = common_ports.get(port, "UNKNOWN")

            open_ports.append(port)

            print(
                colored(
                    f"[OPEN] Port {port} ({service})",
                    "green"
                )
            )

            try:

                banner = sock.recv(1024).decode().strip()

                if banner:

                    print(
                        colored(
                            f" Banner: {banner}",
                            "yellow"
                        )
                    )

            except:
                pass

        else:

            print(
                colored(
                    f"[CLOSED] Port {port}",
                    "red"
                ),
                end='\r'
            )

        sock.close()

    except:
        pass

# ==========================================
# MAIN SCANNER
# ==========================================

def start_scan(target):

    print(
        colored(
            f"\n[-] Starting Real-Time Scan On {target}\n",
            "cyan"
        )
    )

    threads = []

    for port in range(1, 1025):

        t = threading.Thread(
            target=scan_port,
            args=(target, port)
        )

        threads.append(t)

        t.start()

    for t in threads:

        t.join()

    print(
        colored(
            "\n\n[+] SCAN COMPLETED",
            "yellow"
        )
    )

    print(
        colored(
            f"[+] TOTAL OPEN PORTS: {len(open_ports)}",
            "cyan"
        )
    )

# ==========================================
# USER INPUT
# ==========================================

target = input(
    colored(
        "\n[>] Enter Your IP Address: ",
        "yellow"
    )
)

start_scan(target)