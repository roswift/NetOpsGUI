import platform
import subprocess
import re


def get_dns_config() -> list:
    """Retrieve DNS server information based on the operating system.

    Returns:
        list: List of DNS server IPs.
    """
    system = platform.system()
    if system == "Windows":
        try:
            command = 'ipconfig | findstr "Default Gateway"'
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT
            ).decode("utf-8")
            dns_configs = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", output)
            return dns_configs
        except subprocess.CalledProcessError:
            return []
    elif system == "Linux" or system == "Darwin":
        try:
            with open("/etc/resolv.conf") as resolv_conf:
                dns_configs = [
                    line.split()[1]
                    for line in resolv_conf
                    if line.strip().startswith("nameserver")
                ]
                return dns_configs
        except FileNotFoundError:
            return []
    else:
        return []


def main():
    dns_configs = get_dns_config()
    if dns_configs:
        print("DNS Settings:")
        for server in dns_configs:
            print(server)
    else:
        print("DNS server information not found.")


if __name__ == "__main__":
    main()
