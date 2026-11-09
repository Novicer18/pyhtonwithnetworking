from scapy.all import IP, ICMP, sr1

def send_custom_ping(target_ip, custom_message):
    print(f"[*] Crafting custom packet for {target_ip}...")
    
    # Layer 3 (IP) + Layer 4 (ICMP) + Application Payload Data
    custom_packet = IP(dst=target_ip) / ICMP() / custom_message
    
    # Send packet and wait for the response
    print("[*] Injecting packet into network...")
    reply = sr1(custom_packet, timeout=2)
    
    if reply:
        print("[+] Received Reply!")
        # Display the full structure of the response packet
        reply.show()
    else:
        print("[-] No response from host.")

# Example usage
send_custom_ping("10.240.72.148", "Hello from Scapy!")
