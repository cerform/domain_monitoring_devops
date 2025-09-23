
import requests

import ssl
import socket
from datetime import datetime, timezone
import json
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_status(domain):
    try:    
        response = requests.get(domain, timeout=5)
        print("Status Code is:", response.status_code)
    except  requests.exceptions.RequestException as e:
            print("Error:", e)

check_status("https://google.com")

def check_ssl(domain):
    try: 

        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                certificate = ssock.getpeercert()
        
        expired_str = certificate['notAfter']
        expire_date = datetime.strptime(expired_str, "%b %d %H:%M:%S %Y %Z")

        if expire_date > datetime.now():
            print(f"SSL for {domain} is VALID till {expire_date}")
        else:
            print(f"SSL for {domain} will EXPIRED on {expire_date}")

    except Exception as e:
            print(f"There is an ERROR checking SSL for {domain}: {e}")

check_ssl("google.com")


