from nslookup import Nslookup, DNSresponse
import logging
import re

### https://github.com/wesinator/pynslookup
### Be sure to change you DNS in the main() function to fit your needs


class SOA:
    """Class representing DNS Data"""

    def __init__(self, soa_response: DNSresponse, logger: logging.Logger = None):
        """_summary_

        Args:
            soa_response (DNSresponse): DNSresponse object from nslookup
            logger (logging.Logger, optional): Optional logger. One will be created if not provided.
        """

        self.soa_data = soa_response.response_full
        self.logger = logging.getLogger("SOA") if logger is None else logger

    def clean_soa_results(self) -> list[str]:
        """Clean SOA response data from nslookup.

        Returns:
            list[str]: List of cleaned SOA data
        """

        cleaned_results = []
        entry = self.soa_data[0]
        split_strings = re.split(r" ", entry)
        for result in split_strings:
            cleaned_results.append(result)
        return cleaned_results

    def print_soa_results(self, cleaned_results: list[str]) -> None:
        # Check if the result list contains at least 11 elements
        if len(cleaned_results) >= 11:
            enriched_results = {
                # Extract individual pieces of information
                "Domain Name": cleaned_results[0],
                "TTL": cleaned_results[1],
                "Record Class": cleaned_results[2],
                "Record Type": cleaned_results[3],
                "Primary Name Server": cleaned_results[4],
                "Responsible Email": cleaned_results[5],
                "Serial Number": cleaned_results[6],
                "Refresh Interval": cleaned_results[7],
                "Retry Interval": cleaned_results[8],
                "Expire Limit": cleaned_results[9],
                "Minimum TTL": cleaned_results[10],
            }
            self.logger.info(enriched_results)
        else:
            self.logger.error(
                f"[RESULT]: {cleaned_results} is invalid result format. Length is < 11"
            )


class DNS:
    """Class representing DNS Data"""

    def __init__(self, dns_response: DNSresponse, logger: logging.Logger = None):
        """Initialize a DNS object.

        Args:
            dns_response (DNSresponse): DNSresponse object from nslookup
            logger (logging.Logger, optional): Optional logger. One will be created if not provided.
        """
        self.dns_data = dns_response.response_full
        self.logger = logging.getLogger("DNS") if logger is None else logger

    def clean_results(self) -> list[str]:
        """Clean DNS response data from nslookup.

        Returns:
            list[str]: List of cleaned DNS data
        """
        cleaned_results = []
        entry = self.dns_data[0]
        split_strings = re.split(r"\n", entry)
        for result in split_strings:
            cleaned_results.append(result)
        return cleaned_results

    def print_dns_results(self, cleaned_results: list[str]) -> None:
        """Format and print cleaned DNS result data

        Args:
            cleaned_results (list[str]): Cleaned DNS result data from 'DNS.clean_results'
        """
        for result in cleaned_results:
            part = result.split()
            if len(result) >= 5:
                enriched_results = {
                    "Domain": part[0],
                    "TTL": part[1],
                    "Type": part[3],
                    "IP": part[4],
                }
                self.logger.info(enriched_results)
            else:
                self.logger.error(
                    f"[RESULT]: {result} is invalid result format. Length is < 4."
                )


def main():
    ### Changes your DNS as needed
    domain_server = ["1.1.1.1"]
    print(
        "[Domain example]: google.com, yahoo.com, youtube.com, speedtest.net, twitch.tv"
    )
    scanned_domain = input("Please provide a Domain to scan: ")
    dns_query = Nslookup(dns_servers=domain_server, verbose=True, tcp=False)

    ### IPv4 and IPv6 DNS Lookup Information
    try:
        dns_v4_results = dns_query.dns_lookup(scanned_domain)
        dns_v4_info = DNS(dns_v4_results)
        cleaned_v4_results = dns_v4_info.clean_results()
        dns_v4_info.print_dns_results(cleaned_v4_results)
    except IndexError:
        print(
            f"[INDEX ERROR]: Unable to obtain IPv4 Lookup Information for provided domain: {scanned_domain}"
        )
    except Exception as e:
        print(f"[GENERIC ERROR]: {e}")

    try:
        dns_v6_results = dns_query.dns_lookup6(scanned_domain)
        dns_v6_info = DNS(dns_v6_results)
        cleaned_v6_results = dns_v6_info.clean_results()
        dns_v6_info.print_dns_results(cleaned_v6_results)
    except IndexError:
        print(
            f"[INDEX ERROR]: Unable to obtain IPv6 Lookup Information for provided domain: {scanned_domain}"
        )
    except Exception as e:
        print(f"[GENERIC ERROR]: {e}")

    ### SOA Lookup Information
    try:
        soa_results = dns_query.soa_lookup(scanned_domain)
        soa_info = SOA(soa_results)
        cleaned_soa_results = soa_info.clean_soa_results()
        soa_info.print_soa_results(cleaned_soa_results)
    except IndexError:
        print(
            f"[INDEX ERROR]: Unable to obtain SOA Lookup Information for provided domain: {scanned_domain}"
        )
    except Exception as e:
        print(f"[GENERIC ERROR]: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

    """
    ### [EXAMPLE OUTPUT] ###
    ### DNS
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '74.6.231.20'}
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '74.6.231.21'}
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '54.161.105.65'}
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '98.137.11.164'}
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '34.225.127.72'}
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '74.6.143.26'}
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '74.6.143.25'}
    {'Domain': 'yahoo.com', 'TTL': '1241', 'Type': 'A', 'IP': '98.137.11.163'}
    {'Domain': 'yahoo.com', 'TTL': '1289', 'Type': 'AAAA', 'IP': '2001:4998:124:1507::f000'}
    {'Domain': 'yahoo.com', 'TTL': '1289', 'Type': 'AAAA', 'IP': '2001:4998:44:3507::8001'}
    {'Domain': 'yahoo.com', 'TTL': '1289', 'Type': 'AAAA', 'IP': '2001:4998:44:3507::8000'}
    {'Domain': 'yahoo.com', 'TTL': '1289', 'Type': 'AAAA', 'IP': '2001:4998:124:1507::f001'}
    {'Domain': 'yahoo.com', 'TTL': '1289', 'Type': 'AAAA', 'IP': '2001:4998:24:120d::1:0'}
    {'Domain': 'yahoo.com', 'TTL': '1289', 'Type': 'AAAA', 'IP': '2001:4998:24:120d::1:1'}
    
    ### SOA
    {
        'Domain Name': 'yahoo.com', 
        'TTL': '1800', 
        'Record Class': 'IN', 
        'Record Type': 'SOA', 
        'Primary Name Server': 'ns1.yahoo.com', 
        'Responsible Email': 'hostmaster.yahoo-inc.com', 
        'Serial Number': '2023090610', 
        'Refresh Interval': '3600', 
        'Retry Interval': '300', 
        'Expire Limit': '1814400', 
        'Minimum TTL': '600',
    }
    

    """
