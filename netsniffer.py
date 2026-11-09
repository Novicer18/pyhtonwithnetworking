from scapy.all import sniff, IP, TCP, UDP

def packet_callback(packet):
    # Check if the packet has an IP layer
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # Identify TCP traffic
        if packet.haslayer(TCP):
            print(f"[TCP] {src_ip}:{packet[TCP].sport} -> {dst_ip}:{packet[TCP].dport}")
            
        # Identify UDP traffic
        elif packet.haslayer(UDP):
            print(f"[UDP] {src_ip}:{packet[UDP].sport} -> {dst_ip}:{packet[UDP].dport}")

print("[*] Starting packet sniffer... Press Ctrl+C to stop.")
# Sniff 10 packets on the network (remove count=10 to sniff indefinitely)
sniff(prn=packet_callback, count=10)
