import ipinfo

### https://github.com/ipinfo/python
### Signing up at ipinfo.io will give you a TOKEN which will enable certain benefits explained here: https://ipinfo.io/pricing
### Uncomment the two lines below and replace the other handler option to use your access token
### access_token = "123456789abcd"
### handler = ipinfo.getHandler(access_token)

handler = ipinfo.getHandler()
ip_address = input("Please provide a valid IPv4 or IPv6 address to check: ")


def print_nested_dict(d, prefix=""):
    for key, value in d.items():
        if isinstance(value, dict):
            print_nested_dict(value, prefix + key + "_")
        else:
            print(prefix + key + ": ", value)


try:
    details = handler.getDetails(ip_address)
    results = details.all
    final_results = {key: value for key, value in results.items() if key != "readme"}
    for key, value in final_results.items():
        if isinstance(value, dict):
            print_nested_dict(value, key + " ")
        else:
            print(key + ": ", value)

except Exception as e:
    print(f"[ERROR]: {e}")


### If you wanted to print out specific items from the dictionary you can do things like: results.ip, results.loc, results.postal etc.

"""
###[EXAMPLE OUTPUT]###

ip:  151.101.2.167
anycast:  True
city:  San Francisco
region:  California
country:  US
loc:  37.7621,-122.3971
org:  AS54113 Fastly, Inc.
postal:  94107
timezone:  America/Los_Angeles
country_name:  United States
isEU:  False
country_flag emoji:  🇺🇸
country_flag unicode:  U+1F1FA U+1F1F8
country_currency code:  USD
country_currency symbol:  $
continent code:  NA
continent name:  North America
latitude:  37.7621
longitude:  -122.3971

"""
