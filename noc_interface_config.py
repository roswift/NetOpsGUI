import psutil
import pandas
import ipaddress


def section_decorator(section_title):
    def decorator(func):
        def wrapper(self):
            print("\n")
            print("#" * 125)
            print(section_title)
            print("#" * 125)
            func(self)

        return wrapper

    return decorator


class localhostconf:
    """Class to create psutil object for later functions"""

    def __init__(self):
        self.connections = psutil.net_connections(kind="inet")
        self.interface_stats = psutil.net_if_stats()
        self.interface_addresses = psutil.net_if_addrs()
        self.io_counters = psutil.net_io_counters()

    @section_decorator("Current Network Connections")
    def network_connections(self) -> pandas.DataFrame:
        """Function used to print the network connections retrieved from:self.connections = psutil.net_connections(kind="inet")
        Returns:
            pandas.DataFrame: Columns include: IP type, Connection Type, Local IP/Port, Remote IP/Port, Status.
        [EXAMPLE OUTPUT]:
        #############################################################################################################################
        Current Network Connections
        #############################################################################################################################
                    Connection Family Connection Type  Local Address  Local Port   Remote Address Remote Port Connection Status
                0                IPv4             TCP      127.0.0.1        1120        127.0.0.1        4102         TIME_WAIT
                1                IPv4             UDP   192.168.11.1        2177                                           NONE
                2                IPv4             TCP   192.168.56.5        3925        127.0.0.1         443       ESTABLISHED
                3                IPv4             TCP      127.0.0.1        1120        127.0.0.1        4084         TIME_WAIT
                4                IPv4             UDP   192.168.86.1        2177                                           NONE
        """
        data = []
        connection_type_map = {1: "TCP", 2: "UDP"}
        connection_family_map = {2: "IPv4", 23: "IPv6"}
        for conn in self.connections:
            local_address, local_port = conn.laddr if conn.laddr else ("", "")
            remote_address, remote_port = conn.raddr if conn.raddr else ("", "")

            data.append(
                {
                    "Connection Family": connection_family_map.get(
                        conn.family, "Unknown"
                    ),
                    "Connection Type": connection_type_map.get(conn.type, "Unknown"),
                    "Local Address": local_address,
                    "Local Port": local_port,
                    "Remote Address": remote_address,
                    "Remote Port": remote_port,
                    "Connection Status": conn.status,
                }
            )

        df = pandas.DataFrame(data)
        print(df)

    @section_decorator("Network Interface Statistics")
    def network_interface_statistics(self) -> pandas.DataFrame:
        """Function used to print the specific interface statistics retrieved from: self.interface_stats = psutil.net_if_stats()

        Returns:
            pandas.DataFrame: Columns include: Interface name, Status, Duplex, Speed, MTU.

        #############################################################################################################################
        Network Interface Statistics
        #############################################################################################################################
                                Interface Status      Duplex  Speed   MTU
        0                       Ethernet   Down  Full Duplex      0  1500
        1                     Ethernet 2     Up  Full Duplex   4294  1500
        2   Bluetooth Network Connection   Down  Full Duplex      3  1500
        3  VMware Network Adapter VMnet1     Up  Full Duplex    100  1500
        4  VMware Network Adapter VMnet8     Up  Full Duplex    100  1500
        5    Loopback Pseudo-Interface 1     Up  Full Duplex   1073  1500
        6                          Wi-Fi   Down  Full Duplex      0  1500
        7       Local Area Connection* 1   Down  Full Duplex      0  1500
        8       Local Area Connection* 2   Down  Full Duplex      0  1500
        """
        status_map = {False: "Down", True: "Up"}
        duplex_map = {1: "Half Duplex", 2: "Full Duplex"}
        data = []
        for interface, stats in self.interface_stats.items():
            data.append(
                {
                    "Interface": interface,
                    "Status": stats.isup,
                    "Duplex": stats.duplex,
                    "Speed": stats.speed,
                    "MTU": stats.mtu,
                }
            )
            df = pandas.DataFrame(data)
            df["Status"] = df["Status"].map(status_map)
            df["Duplex"] = df["Duplex"].map(duplex_map)
        print(df)

    @section_decorator("Network Interface Addresses")
    def network_interface_addresses(self) -> pandas.DataFrame:
        """Function to print the interface addresses retrieved from: self.interface_addresses = psutil.net_if_addrs()

        Returns:
            pandas.DataFrame: Columns include: Interface Name, MAC Address, IPv4 and IPv6 Addresses, Netmask, Broadcast.
        [EXAMPLE OUTPUT]:
        #############################################################################################################################
        Network Interface Addresses
        #############################################################################################################################
                               Interface        MAC Address     IPv4 Address               IPv6 Address Netmask Broadcast
        0                       Ethernet  ##-##-##-##-##-##   169.254.187.81  fe80::0000:0000:0000:0000    None      None
        1                     Ethernet 2  ##-##-##-##-##-##     192.168.80.2  fe80::0000:0000:0000:0000    None      None
        2                          Wi-Fi  ##-##-##-##-##-##     169.254.17.2  fe80::0000:0000:0000:0000    None      None
        3       Local Area Connection* 1  ##-##-##-##-##-##     169.254.88.2  fe80::0000:0000:0000:0000    None      None
        4       Local Area Connection* 2  ##-##-##-##-##-##    169.254.239.2  fe80::0000:0000:0000:0000    None      None
        5  VMware Network Adapter VMnet1  ##-##-##-##-##-##    192.168.100.1  fe80::0000:0000:0000:0000    None      None
        6  VMware Network Adapter VMnet8  ##-##-##-##-##-##    192.168.101.1  fe80::0000:0000:0000:0000    None      None
        7   Bluetooth Network Connection  ##-##-##-##-##-##  169.254.254.100  fe80::0000:0000:0000:0000    None      None
        8    Loopback Pseudo-Interface 1               None        127.0.0.1                        ::1    None      None
        """
        data = []
        for interface, addresses in self.interface_addresses.items():
            ipv4_address = None
            ipv6_address = None
            mac_address = None

            for addr in addresses:
                try:
                    if ipaddress.ip_address(addr.address).version == 4:
                        ipv4_address = addr.address
                    elif ipaddress.ip_address(addr.address).version == 6:
                        ipv6_address = addr.address
                except:
                    mac_address = addr.address

            data.append(
                {
                    "Interface": interface,
                    "MAC Address": mac_address,
                    "IPv4 Address": ipv4_address,
                    "IPv6 Address": ipv6_address,
                    "Netmask": addr.netmask,
                    "Broadcast": addr.broadcast,
                }
            )
        df = pandas.DataFrame(data)
        print(df)


def main():
    conf = localhostconf()
    conf.network_connections()
    conf.network_interface_statistics()
    conf.network_interface_addresses()


if __name__ == "__main__":
    main()
