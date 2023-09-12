from scapy.all import *
from multiprocessing.pool import ThreadPool
from common_ports import top_100_tcp_ports, top_100_udp_ports
import ipaddress

open_ports = []


def ping_target(target_ip) -> str:
    ping_packet = IP(dst=target_ip) / ICMP()
    ping_response = sr1(ping_packet, timeout=1, verbose=False)
    if ping_response:
        print(f"[{target_ip}] is online")
        return target_ip
    else:
        print(f"[{target_ip}] is offline. Select a new target.")


def is_valid_ip(target_ip) -> str:
    try:
        ipaddress.ip_address(target_ip)
        return target_ip
    except ValueError:
        print(f"The provided IP Address[{target_ip}] is not valid.")


def port_scan(target_port):
    try:
        # TCP port scan
        tcp_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
        tcp_response = sr(tcp_packet, timeout=1, verbose=False)[0]

        # UDP port scan
        udp_packet = IP(dst=target_ip) / UDP(dport=target_port)
        udp_response = sr(udp_packet, timeout=1, verbose=False)[0]

        for sent_packet, received_packet in tcp_response:
            if received_packet.haslayer(TCP) and received_packet[TCP].flags == 0x12:
                print(f"[TCP] port [{target_port}] is up!")
                open_ports.append((target_port, "TCP"))
            else:
                print(f"[TCP] port [{target_port}] is down")

        for sent_packet, received_packet in udp_response:
            if received_packet.haslayer(UDP):
                print(f"[UDP] port [{target_port}] is up!")
                open_ports.append((target_port, "UDP"))

    except Exception as e:
        print(f"[ERROR]: {e}")


def main():
    global target_ip
    target_ip = input("Please provide a target IP: ")
    is_valid_ip(target_ip)
    target_ports_input = input(
        "Please provide a list of ports to scan -OR- Top 100 -OR- ALL: "
    )

    if target_ports_input == "ALL":
        target_ports = list(range(1, 65536))
    elif target_ports_input == "Top 100":
        target_ports = list(set(top_100_tcp_ports + top_100_udp_ports))
    else:
        target_ports = [
            int(port)
            for port in target_ports_input.split(",")
            if port.strip().isdigit()
        ]

    ping_target(target_ip)
    try:
        with ThreadPool() as pool:
            pool.map(port_scan, target_ports)
    except KeyboardInterrupt:
        print("User exited code execution")

    print("#############################")
    print("#########OPEN PORTS##########")
    print("#############################")
    for port, protocol in open_ports:
        print(f"[{port}] is open ({protocol})")
    print("#############################")


if __name__ == "__main__":
    main()
