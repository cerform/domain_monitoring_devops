import os
import requests

# Base URL configuration
# Default to localhost:8080 if no environment variable is set
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")



# GET webpage

def check_get_webpage(path="/"):
    """
    Send a GET request to the specified path using the base URL.
    Example: check_get_webpage("/login")
    """
    url = f"{BASE_URL}{path}"
    response = requests.get(url)
    return response



# User registration

def check_register_user(name, password, password_confirmation):
    """
    Send a POST request to /register to create a new user.
    """
    url = f"{BASE_URL}/register"
    payload = {
        "username": name,
        "password": password,
        "password_confirmation": password_confirmation
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    return response



# User login

def check_login_user(name, password):
    url = f"{BASE_URL}/login"
    payload = {
        "username": name,
        "password": password
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    return response



# Dashboard access

def check_dashboard(session_cookie):
    """
    Send a GET request to /dashboard using the provided session cookie.
    """
    url = f"{BASE_URL}/dashboard"
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

    url = f"{BASE_URL}/scan_domains"
    cookies = {}

    if session_cookie:
        cookies["session"] = session_cookie

    response = requests.get(url, cookies=cookies, timeout=5)
    return response 


