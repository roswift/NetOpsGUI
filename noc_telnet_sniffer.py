from scapy.all import *
from datetime import datetime

num_telnets_in = []
num_telnets_out = []
packet_number = 0


def telnet_monitor_callback(pcap):
    global packet_number
    for pkt in pcap:
        packet_number += 1
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d | %H:%M:%S.%f")[:-3]
        if pkt.haslayer(TCP) and pkt[TCP].dport == 23:
            try:
                sent_telnet = pkt.load.decode("utf-8")
                if sent_telnet:
                    print(f"{packet_number} | {timestamp} | [Telnet]: {sent_telnet}")
                else:
                    pass
            except UnicodeDecodeError:
                pass
            except AttributeError:
                pass
            num_telnets_out.append(pkt)
        elif pkt.haslayer(TCP) and pkt[TCP].sport == 23:
            # Extract and decode the Telnet payload as ASCII
            try:
                telnet_payload = pkt.load.decode("utf-8")
                if len(telnet_payload) > 1:
                    print(f"{packet_number} | {timestamp} | [Telnet]: {telnet_payload}")
            except UnicodeDecodeError:
                pass
            except AttributeError:
                pass
            num_telnets_in.append(pkt)
        else:
            pass


def display_telnet(pkt):
    return pkt.haslayer(TCP) and (pkt[TCP].dport == 23 or pkt[TCP].sport == 23)


def telnet_capture():
    try:
        sniff(prn=telnet_monitor_callback, iface="Ethernet 2", lfilter=display_telnet)

    except KeyboardInterrupt:
        print("sniff() cancelled by user input")


def main():
    telnet_capture()
    print("Number of Telnet Packets IN:", len(num_telnets_in))
    print("Number of Telnet Packets OUT:", len(num_telnets_out))


if __name__ == "__main__":
    main()
