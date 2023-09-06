from nslookup import Nslookup
import re

class SOA:
    def __init__(self, args):
        self.args = args

    def clean_results(self):
        cleaned_results = []
        entry = self.args[0]
        split_strings = re.split(r" ", entry)
        for result in split_strings:
            result = result.replace(".com.", ".com")
            cleaned_results.append(result)
        return cleaned_results

    def enrich_soa_results(self, result):
        results = {}
        # Check if the result list contains at least 11 elements
        if len(result) >= 11:
            # Extract individual pieces of information
            results["Domain Name"] = result[0]
            results["TTL"] = result[1]
            results["Record Class"] = result[2]
            results["Record Type"] = result[3]
            results["Primary Name Server"] = result[4]
            results["Responsible Email"] = result[5]
            results["Serial Number"] = result[6]
            results["Refresh Interval"] = result[7]
            results["Retry Interval"] = result[8]
            results["Expire Limit"] = result[9]
            results["Minimum TTL"] = result[10]
        else:
            print("Invalid result format:", result)
        print(results)
        return results


class DNS:
    def __init__(self, args):
        self.args = args

    def clean_results(self):
        cleaned_results = []
        entry = self.args[0]
        split_strings = re.split(r"\n", entry)
        for result in split_strings:
            result = result.replace(".com.", ".com")
            cleaned_results.append(result)
        return cleaned_results

    def enrich_v4_results(self, result):
        parts = result.split()
        if len(parts) >= 5:
            enriched_results = {
                "Domain": parts[0],
                "TTL": parts[1],
                "Type": parts[3],
                "IP": parts[4],
            }
            print(enriched_results)
        else:
            print("Invalid result format:", result)

    def enrich_v6_results(self, result):
        parts = result.split()
        if len(parts) >= 5:
            enriched_results = {
                "Domain": parts[0],
                "TTL": parts[1],
                "Type": parts[3],
                "IP": parts[4],
            }
            print(enriched_results)
        else:
            print("Invalid result format:", result)


def main():
    domain_server = ["1.1.1.1"]
    scanned_domain = input("Please provide a Domain to scan: ")
    dns_query = Nslookup(dns_servers=domain_server, verbose=True, tcp=False)

    ### IPv4 DNS Lookup Information
    try:
        dns_results_v4 = dns_query.dns_lookup(scanned_domain)
        dns_v4_full = dns_results_v4.response_full
        dns_v4_info = DNS(dns_v4_full)
        cleaned_v4_results = dns_v4_info.clean_results()
        for result in cleaned_v4_results:
            dns_v4_info.enrich_v4_results(result)
    except IndexError:
        print(
            f"[ERROR]: Unable to obtain IPv4 Lookup Information for provided domain: {scanned_domain}"
        )
    except Exception as e:
        print(f"[ERROR]: {e}")
    ### IPv6 DNS Lookup Information
    try:
        dns_results_v6 = dns_query.dns_lookup6(scanned_domain)
        dns_v6_full = dns_results_v6.response_full
        dns_v6_info = DNS(dns_v6_full)
        cleaned_v6_results = dns_v6_info.clean_results()
        for result in cleaned_v6_results:
            dns_v6_info.enrich_v6_results(result)
    except IndexError:
        print(
            f"[ERROR]: Unable to obtain IPv6 Lookup Information for provided domain: {scanned_domain}"
        )
    except Exception as e:
        print(f"[ERROR]: {e}")
    ### SOA Lookup Information
    try:
        soa_results = dns_query.soa_lookup(scanned_domain)
        soa_full = soa_results.response_full
        soa_info = SOA(soa_full)
        cleaned_soa_results = soa_info.clean_results()
        soa_info.enrich_soa_results(cleaned_soa_results)
    except IndexError:
        print(
            f"[ERROR]: Unable to obtain SOA Lookup Information for provided domain: {scanned_domain}"
        )
    except Exception as e:
        print(f"[ERROR]: {e}")


if __name__ == "__main__":
    main()
