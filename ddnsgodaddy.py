#!/usr/bin/env python3
import datetime
import os
import requests

def validipaddress(ipaddress):
    try:
        parts = ipaddress.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False # one of the 'parts' not convertible to integer
    except (AttributeError, TypeError):
        return False # not a string


def printdnsrecords(apiurl, headers, prefix="", ipmatch=None):
    updaterequired = True
    with requests.get(apiurl, headers=headers) as r:
        assert(r.status_code == 200)
        for record in r.json():
            print(f"{prefix:25s}{record['name']}  {record['type']}  {record['data']}  TTL: {record['ttl']}")
            if record['data'] == ipmatch:
                updaterequired = False

    return updaterequired


def main():
    key = os.environ['GODADDY_KEY']
    secret = os.environ['GODADDY_SECRET']

    authheader = {
        "Authorization": f"sso-key {key}:{secret}",
        "Content-type": "application/json"}

    domain = "lukeshingles.com"

    # hostname, or @ for apex domain
    hostname = "mbp2012"

    # Time To Live in seconds
    ttl = 600

    print(f"Starting at local time {datetime.datetime.now().isoformat()}")

    get_ip_url = "http://api.ipify.org"

    with requests.get(get_ip_url) as r:
        assert(r.status_code == 200)
        ipaddress = r.text
        assert(validipaddress(ipaddress))

    print(f"External IP address is {ipaddress}")

    apiurl = f"https://api.godaddy.com/v1/domains/{domain}/records/A/{hostname}"
    updaterequired = printdnsrecords(apiurl, authheader, prefix="GoDaddy DNS before: ", ipmatch=ipaddress)

    if not updaterequired:
            print("(no update needed)")
    else:
        newrecords = [{ "data": ipaddress, "ttl": ttl, "name": hostname, "type": "A" },]
        with requests.put(apiurl, headers=authheader, json=newrecords) as r:
            assert(r.status_code == 200)

        printdnsrecords(apiurl, authheader, prefix="GoDaddy DNS after: ")

    print("")


main()
