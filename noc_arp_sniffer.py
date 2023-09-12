from scapy.all import *
from datetime import datetime

packet_number = 0
num_arp_requests = []
num_arp_replies = []


def arp_monitor_callback(pkt):
    global packet_number
    if ARP in pkt:
        arp_pkt = pkt[ARP]
        packet_number += 1
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d | %H:%M:%S.%f")[:-3]
        if arp_pkt.op == 1:  # 1 corresponds to ARP request : op = who-has
            print(
                f"{packet_number} | {timestamp} | [ARP]: Request ==> {arp_pkt.psrc} is asking for {arp_pkt.pdst}"
            )
            num_arp_requests.append(arp_pkt)
            return None
        elif arp_pkt.op == 2:  # 2 corresponds to ARP reply op = is-at
            print(
                f"{packet_number} | {timestamp} | [ARP]: Reply <== {arp_pkt.hwsrc} is at {arp_pkt.psrc}"
            )
            num_arp_replies.append(arp_pkt)
            return None


def arp_capture():
    try:
        sniff(
            prn=arp_monitor_callback,
            filter="arp",
            iface="Ethernet 2",
            store=0,
        )
    except KeyboardInterrupt:
        print("sniff() cancelled by user input")


def main():
    arp_capture()
    print("Number of ARP Replies:", len(num_arp_replies))
    print("Number of ARP Requests:", len(num_arp_requests))


if __name__ == "__main__":
    main()
