import ipinfo

### https://github.com/ipinfo/python
### Signing up at ipinfo.io will give you a TOKEN which will enable certain benefits explained here: https://ipinfo.io/pricing
### Uncomment the two lines below and replace the other handler option to use your access token
### access_token = "123456789abcd"
### handler = ipinfo.getHandler(access_token)

handler = ipinfo.getHandler()
ip_address = input("Please provide a valid IPv4 or IPv6 address to check: ")
try:
    details = handler.getDetails(ip_address)
    results = details.all
    ### Filter out 'readme' from results. The 'readme' key includes data about using an auth-token provided by signing up at ipinfo.io
    final_results = {key: value for key, value in results.items() if key != "readme"}
    print(final_results)
except Exception as e:
    print(f"[ERROR]: {e}")

### If you wanted to print out specific items from the dictionary you can do things like: results.ip, results.loc, results.postal etc.

"""
###[EXAMPLE OUTPUT]###

{
    'ip': '8.8.8.8', 
    'hostname': 'dns.google', 
    'anycast': True, 
    'city': 'Mountain View', 
    'region': 'California', 
    'country': 'US', 
    'loc': '37.4056,-122.0775', 
    'org': 'AS15169 Google LLC', 
    'postal': '94043', 
    'timezone': 
    'America/Los_Angeles', 
    'readme': 'https://ipinfo.io/missingauth', 
    'country_name': 'United States', 
    'isEU': False, 
    'country_flag': {'emoji': '🇺🇸', 
    'unicode': 'U+1F1FA U+1F1F8'}, 
    'country_currency': {'code': 'USD', 
                        'symbol': '$'}, 
    'continent': {'code': 'NA', 
                'name': 'North America'}, 
    'latitude': '37.4056', 
    'longitude': '-122.0775'},
}

"""
