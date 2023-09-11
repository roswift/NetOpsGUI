import platform
import re


def get_dns_config() -> list:
    """Run Subprocess: ipconfig /all or read the /etc/resolv.conf file to obtain the current DNS server on the computer.

    Returns:
        list: returns a list to use in the noc_nslookup.py file.
    """
    system = platform.system()
    if system == "Windows":
        import subprocess

        try:
            output = subprocess.check_output(["ipconfig", "/all"]).decode("utf-8")
            dns_servers = re.findall(r"DNS Server(.*?)\n", output, re.DOTALL)[0].strip()
            return [dns_servers.split()[-1]]
        except subprocess.CalledProcessError:
            return []

    elif system == "Linux" or system == "Darwin":
        with open("/etc/resolv.conf") as resolv_confg:
            lines = resolv_confg.readlines()
            dns_servers = [
                line.strip().split()[1]
                for line in lines
                if line.startswith("nameserver")
            ]
            return dns_servers
    else:
        return []


def main():
    dns_servers = get_dns_config()
    if dns_servers:
        print(dns_servers)
    else:
        print("DNS server information not found.")


if __name__ == "__main__":
    main()
