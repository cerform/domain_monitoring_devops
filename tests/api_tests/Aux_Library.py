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