import ipinfo

### https://github.com/ipinfo/python
### Signing up at ipinfo.io will give you a TOKEN which will enable certain benefits explained here: https://ipinfo.io/pricing
### Uncomment the two lines below and replace the other handler option to use your access token
### access_token = "123456789abcd"
### handler = ipinfo.getHandler(access_token)


class IPinfo:
    """Class to create IPinfo API handler"""

    def __init__(self, ip: str):
        self.ip = ip
        self.handler = ipinfo.getHandler()
        self.details = self.handler.getDetails(self.ip)
        ### If you wanted to retrieve specific items from the dictionary you can do things like: results.ip, results.loc, results.postal etc
        ### In my case, I want to retrieve '.all' items from the API.
        self.results = self.flatten_dict(self.details.all)

    def flatten_dict(self, results: dict, parent_key="", seperator="_") -> dict:
        """The raw values contain nested dicts for certain values. This function aims to flatten them,
           and produce individual line items as output.

        Args:
            results (dict): Results from the self.details = self.handler.getDetails(self.ip). Using the '.all' attribute for details (self.details.all).
            parent_key (str, optional): The parent key would be things like "country_flag", "country_currency", and "continent". Defaults to "".
            seperator (str, optional): The deliminator of choice to join the values together. Defaults to "_".

        Returns:
            dict: takes in the results dict, and flattens the nested items to produce single outputs.

        [EXAMPLE OUTPUT]:
            ip: 8.8.8.8
            hostname: dns.google
            anycast: True
            city: Mountain View
            region: California
            country: US
            loc: 37.4056,-122.0775
            org: AS15169 Google LLC
            postal: 94043
            timezone: America/Los_Angeles
            country_name: United States
            isEU: False
            country_flag_emoji: 🇺🇸
            country_flag_unicode: U+1F1FA U+1F1F8
            country_currency_code: USD
            country_currency_symbol: $
            continent_code: NA
            continent_name: North America
            latitude: 37.4056
            longitude: -122.0775
            longitude:  -122.0775

        """

        items = {}
        for key, value in results.items():
            new_key = f"{parent_key}{seperator}{key}" if parent_key else key
            if isinstance(value, dict):
                items.update(self.flatten_dict(value, new_key, seperator=seperator))
            else:
                items[new_key] = value
        return items

    def print_api_get(self):
        """Function is currently designed to print to terminal. Intended use case it to interact with GUI after more development"""
        try:
            for key, value in self.results.items():
                ### Discard the "readme" key. Only provides a link to incorporate token authentication.
                if key != "readme":
                    print(f"{key}: {value}")

            else:
                print(key + ": ", value)
        except Exception as e:
            print(f"[ERROR]: {e}")


def main():
    ip_address = input("Please provide a valid IPv4 or IPv6 address to check: ")
    ipinfo_get = IPinfo(ip_address)
    ipinfo_get.print_api_get()


if __name__ == "__main__":
    main()
