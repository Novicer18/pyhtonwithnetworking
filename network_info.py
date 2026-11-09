import os
import platform
import re
import socket
import subprocess
import uuid


def get_wifi_ip():
    """Finds and returns the specific IP address assigned to the Wi-Fi card."""
    os_type = platform.system()
    
    if os_type == "Windows":
        try:
            # Run 'ipconfig' to look at network adapters
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
            # Find the section for the Wireless LAN adapter
            sections = result.stdout.split("\n\n")
            for section in sections:
                if "Wireless LAN adapter Wi-Fi" in section or "Wireless LAN adapter" in section:
                    # Look for the IPv4 Address line inside the Wi-Fi section
                    ip_match = re.search(r"IPv4 Address[\.\s]*:\s*([\d\.]+)", section)
                    if ip_match:
                        return ip_match.group(1).strip()
        except Exception:
            pass

    # Fallback method for Mac, Linux, and Windows if ipconfig fails
    try:
        # We simulate connecting to an outside internet address (without actually sending data)
        # This forces the OS to tell us which specific adapter it is using to route traffic.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        wifi_ip = s.getsockname()[0]
        s.close()
        return wifi_ip
    except Exception:
        return "Unknown (Not Connected to a network)"


def get_network_info():
    print("=" * 40)
    print(" CORE NETWORK INFORMATION")
    print("=" * 40)

    # 1. Hostname & Specific Wi-Fi IP Address
    hostname = socket.gethostname()
    wifi_ip = get_wifi_ip()

    print(f"Hostname: {hostname}")
    print(f"Actual Wi-Fi IP Address: {wifi_ip}")  # <--- Changed here

    # 2. MAC Address
    mac_num = hex(uuid.getnode()).replace("0x", "").upper().zfill(12)
    mac_address = ":".join(mac_num[i : i + 2] for i in range(0, 11, 2))
    print(f"MAC Address: {mac_address}")


def get_wifi_details():
    print("\n" + "=" * 40)
    print(" WI-FI DETAILS & SECURITY")
    print("=" * 40)

    os_type = platform.system()
    ssid = "Not Connected / Unknown"
    password = "Could not retrieve (Requires Admin/Sudo)"

    try:
        if os_type == "Windows":
            cmd_ssid = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
            ssid_match = re.search(r"SSID\s*:\s*(.*)", cmd_ssid.stdout)

            if ssid_match:
                ssid = ssid_match.group(1).strip()
                cmd_pass = subprocess.run(["netsh", "wlan", "show", "profile", f"name={ssid}", "key=clear"], capture_output=True, text=True)
                pass_match = re.search(r"Key Content\s*:\s*(.*)", cmd_pass.stdout)
                if pass_match:
                    password = pass_match.group(1).strip()

        elif os_type == "Darwin":  # macOS
            cmd_ssid = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"], capture_output=True, text=True)
            ssid_match = re.search(r" SSID: (.*)", cmd_ssid.stdout)

            if ssid_match:
                ssid = ssid_match.group(1).strip()
                cmd_pass = subprocess.run(["security", "find-generic-password", "-D", "AirPort network password", "-wa", ssid], capture_output=True, text=True)
                if cmd_pass.returncode == 0:
                    password = cmd_pass.stdout.strip()

        elif os_type == "Linux":
            cmd_ssid = subprocess.run(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], capture_output=True, text=True)
            for line in cmd_ssid.stdout.splitlines():
                if line.startswith("yes:"):
                    ssid = line.split(":")[1].strip()
                    break

            if ssid and ssid != "Not Connected / Unknown":
                cmd_pass = subprocess.run(["sudo", "nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid], capture_output=True, text=True)
                if cmd_pass.returncode == 0 and cmd_pass.stdout.strip():
                    password = cmd_pass.stdout.strip()

    except Exception as e:
        password = f"Error extracting details: {str(e)}"

    print(f"Wi-Fi SSID (Name): {ssid}")
    print(f"Wi-Fi Password:    {password}")


if __name__ == "__main__":
    get_network_info()
    get_wifi_details()
