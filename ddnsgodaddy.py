#!/usr/bin/env python3
import datetime
import requests

def validipaddress(ipaddress):
    try:
        parts = ipaddress.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False # one of the 'parts' not convertible to integer
    except (AttributeError, TypeError):
        return False # not a string

def printrecords(records):
    for record in records:
        print(f"  {record['name']}  {record['type']}  {record['data']}  TTL: {record['ttl']}")

def main():
    key = "KEY"
    secret = "SECRET"

    authheader = {
        "Authorization": f"sso-key {key}:{secret}",
        "Content-type": "application/json"}

    domain = "lukeshingles.com"

    # hostname, or @ for apex domain
    hostname = "mbp2012"

    # Time To Live in seconds
    ttl = 600

    print(f"Starting at local time {datetime.datetime.now().isoformat()}\n")

    get_ip_url = "http://api.ipify.org"

    with requests.get(get_ip_url) as r:
        assert(r.status_code == 200)
        ipaddress = r.text
        assert(validipaddress(ipaddress))

    print(f"External IP address: {ipaddress}")

    apiurl = f"https://api.godaddy.com/v1/domains/{domain}/records/A/{hostname}"

    print()

    with requests.get(apiurl, headers=authheader) as r:
        assert(r.status_code == 200)
        print("GoDaddy current records:")
        printrecords(r.json())

    print()

    newrecords = [{ "data": ipaddress, "ttl": ttl, "name": hostname, "type": "A" },]
    with requests.put(apiurl, headers=authheader, json=newrecords) as r:
        assert(r.status_code == 200)
        print("GoDaddy new records:")
        printrecords(newrecords)

    print("\n-----\n")


main()
