# 🔍 Local Network Scanner — `h0sc4nner.py`

![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux--only-lightgrey)

A Python tool to scan your local network, discover live hosts, and identify devices.

---

## ✅ Features

- Auto-detects your local subnet
- Scans a specified number of IPs
- Uses ARP to find live devices
- Retrieves MAC addresses and vendors
- Uses `nmap` to resolve hostnames (only for online devices)
- Outputs a clean table with:
  - IP Address
  - MAC Address
  - Vendor
  - Hostname

---

## ⚙️ Requirements

- Linux (due to `arping` dependency)
- Python 3.7+
- Tools:
  - `nmap`
  - `arping`
- Python packages:
  - `scapy`
  - `requests`
  - `tabulate`
  - `netifaces`

### Install Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip nmap arping -y
pip install -r requirements.txt
```

📄 `requirements.txt`
```
scapy
requests
tabulate
netifaces
```

---

## 🚀 Usage

Run the tool with `sudo`:

```bash
sudo python3 h0sc4nner.py <number_of_ips_to_scan>
```

Example:

```bash
sudo python3 h0sc4nner.py 50
```

Scans the first 50 IPs in your local subnet (e.g., `192.168.1.1` to `192.168.1.50`).

> ⚠️ Must be run with `sudo` to access ARP functionality.

---

## 🖥️ Example Output

```
Scanning 192.168.1.1 to 192.168.1.50...

+---------------+-------------------+------------------------+--------------------+
| IP Address    | MAC Address       | Vendor                 | Nmap Hostname      |
+---------------+-------------------+------------------------+--------------------+
| 192.168.1.1   | 00:11:22:33:44:55 | Cisco Systems          | router.local       |
| 192.168.1.10  | aa:bb:cc:dd:ee:ff | Apple Inc.             | iPhone.local       |
| 192.168.1.23  | 66:77:88:99:aa:bb | Samsung Electronics    | samsung-tv.local   |
+---------------+-------------------+------------------------+--------------------+
```

---

## 🔍 How It Works

1. Detects your primary network interface and local subnet via `netifaces`
2. Pings the first N IPs using `arping` or ARP requests via Scapy
3. Collects MAC addresses from ARP responses
4. Uses `macvendors.co` to identify MAC vendors
5. Runs `nmap -sP` only on live IPs to resolve hostnames
6. Displays the final output using `tabulate`

---

## 🛠 Troubleshooting

### Script must be run as root:

```bash
sudo python3 h0sc4nner.py 50
```

### `arping` not installed:

```bash
sudo apt install arping
```

### `nmap` not installed:

```bash
sudo apt install nmap
```

### Vendor not displayed:

- Make sure you're connected to the internet (vendor data is fetched via API)

---

## 🤝 Contributing

Pull requests welcome. To contribute:

1. Fork the repo
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit and push changes
4. Open a Pull Request

---


## 📝 License

Licensed under the **MIT License**.
