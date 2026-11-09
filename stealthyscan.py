from scapy.all import IP, TCP, sr1

def syn_scan(target_ip, port):
    # Craft an IP packet to target, containing a TCP SYN packet
    packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
    
    # Send the packet and wait for a single response
    response = sr1(packet, timeout=1, verbose=False)
    
    if response and response.haslayer(TCP):
        # Check if the target replied with a SYN-ACK (Flags 0x12)
        if response[TCP].flags == 0x12:
            print(f"[+] Port {port} is OPEN (SYN-ACK received)")
            
            # Immediately send a RST (Reset) packet to close the half-open connection stealthily
            rst_packet = IP(dst=target_ip) / TCP(dport=port, flags="R")
            send(rst_packet, verbose=False)
        # Check if target replied with a RST-ACK (Flags 0x14)
        elif response[TCP].flags == 0x14:
            print(f"[-] Port {port} is CLOSED")
    else:
        print(f"[-] Port {port} is FILTERED (No response/Dropped by firewall)")

# Example usage (Scan HTTP port 80 on a local router or test machine)
syn_scan("10.240.72.148", 3000)
