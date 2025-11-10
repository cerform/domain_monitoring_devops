import requests

# API Test Script
# Tests the retrieval of a webpage
def check_get_webpage(path="/"):
    response = requests.get(f"http://localhost:8080{path}")
    return response

# Tests user registration
def check_register_user(name, password, password_confirmation):
    url = "http://localhost:8080/register"
    payload = {
        "username": name,
        "password": password,
        "password_confirmation": password_confirmation
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response

# Test login
def check_login_user(name, password):
    url = "http://localhost:8080/login"
    payload = {
        "username": name,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response

#Test Domain retrieval (non expected)
def check_dashboard(session_cookie):
    url = "http://localhost:8080/dashboard"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"session={session_cookie}"
    }

    response = requests.get(url, headers=headers)
    return response


def check_scan_domains(session_cookie: str | None = None):

    """
    Performs a GET request to scan_domains.
    If a session_cookie is provided, sends it as a Flask 'session' cookie.
    Returns the response object from the requests library.
    """

    url = f"http://localhost:8080/scan_domains"
    cookies = {}

    if session_cookie:
        cookies["session"] = session_cookie

    response = requests.get(url, cookies=cookies, timeout=5)
    return response 


