#!/usr/bin/env python3

import datetime
import os
import requests


def validipaddress(ipaddress):
    try:
        parts = ipaddress.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False  # one of the 'parts' not convertible to integer
    except (AttributeError, TypeError):
        return False  # not a string

def main():
    username = os.environ['DDNS_USERNAME']
    password = os.environ['DDNS_PASSWORD']

    headers = {
        "Content-type": "application/json"
    }

    domain = "lukeshingles.com"

    # hostname, or @ for apex domain
    hostname = "home"

    print(f"Starting at local time {datetime.datetime.now().isoformat()}")


    apiurl = (f"https://domains.google.com/nic/"
              f"update?hostname={hostname}.{domain}")

    # Google domains will use the requesting IP address by default.
    # Alternatively, we can find it this way:
    # with requests.get("http://api.ipify.org") as r:
    #     assert(r.status_code == 200)
    #     ipaddress = r.text
    #     assert(validipaddress(ipaddress))
    #
    # print(f"External IP address is {ipaddress}")
    # apiurl += f'&myip={ipaddress}'

    with requests.get(apiurl, headers=headers, auth=(username, password)) as r:
        print(f'{r.status_code} response from {apiurl}')
        print(f'  {r.text}')

    print("")


if __name__ == "__main__":
    main()
