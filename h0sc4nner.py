import os
import sys
import requests
import netifaces
import subprocess
from scapy.all import ARP, Ether, srp

def get_base_ip():
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        if netifaces.AF_INET in netifaces.ifaddresses(iface):
            inet_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
            ip = inet_info['addr']
            if ip != "127.0.0.1":
                parts = ip.split('.')
                return f"{parts[0]}.{parts[1]}.{parts[2]}"
    raise Exception("Could not determine local IP base")

def ping_ip(ip):
    result = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    return result == 0

def scan_range(start_ip, end_ip):
    print(f"[*] Sending ARP requests from {start_ip} to {end_ip}...\n")
    targets = [f"{start_ip.rsplit('.', 1)[0]}.{i}" for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1)]
    arp = ARP(pdst=targets)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    for sent, received in result:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })
    return devices

def get_vendor(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}", timeout=5)
        return response.text if response.status_code == 200 else "Unknown"
    except:
        return "Unknown"

def get_nmap_hostname(ip):
    """Returns nmap-reported hostname from nmap -A output."""
    try:
        output = subprocess.check_output(
            ['nmap', '-A', ip],
            stderr=subprocess.DEVNULL, timeout=40
        ).decode()
        for line in output.splitlines():
            if line.startswith("Nmap scan report for"):
                parts = line[len("Nmap scan report for "):].strip()
                if '(' in parts and ')' in parts:
                    return parts.split('(')[0].strip()
                else:
                    return parts
        return "Unknown"
    except Exception:
        return "Unknown"

def main():
    if len(sys.argv) != 2:
        print("Usage: sudo python run.py <number_of_ips_to_scan>")
        sys.exit(1)

    try:
        count = int(sys.argv[1])
        if count < 1 or count > 254:
            raise ValueError
    except ValueError:
        print("Error: Enter a number between 1 and 254")
        sys.exit(1)

    base_ip = get_base_ip()
    start_ip = f"{base_ip}.1"
    end_ip = f"{base_ip}.{count}"

    print(f"[*] Scanning IP range: {start_ip} to {end_ip}")

    print("\n[*] Pinging devices...")
    for i in range(1, count + 1):
        ip = f"{base_ip}.{i}"
        print(f"[+] Pinging {ip}...", end="", flush=True)
        if ping_ip(ip):
            print(" reachable!")
        else:
            print(" no response!")

    # ARP scan for MAC addresses
    devices = scan_range(start_ip, end_ip)

    print(f"\n{'IP Address':<16} {'MAC Address':<20} {'Vendor':<30} {'Nmap Hostname':<30}")
    print("-" * 100)

    for device in devices:
        ip = device['ip']
        mac = device['mac']
        vendor = get_vendor(mac)
        nmap_hostname = get_nmap_hostname(ip)
        print(f"{ip:<16} {mac:<20} {vendor:<30} {nmap_hostname:<30}")

if __name__ == "__main__":
    main()