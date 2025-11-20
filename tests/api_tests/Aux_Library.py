import os
import requests
import re
import json
from UserManagementModule import UserManager as UM

# -----------------------------------------------------
# Base URL (inside Docker container app runs on 0.0.0.0:8080)
# -----------------------------------------------------
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")


# -----------------------------------------------------
# Create a NEW session for each request (fixes cookie conflicts)
# -----------------------------------------------------
def new_session():
    return requests.Session()


# -----------------------------------------------------
# Utility Functions
# -----------------------------------------------------
def extract_cookie(response):
    """
    Extract session cookie from response headers.
    Returns token or None.
    """
    cookie_header = response.headers.get("Set-Cookie", "")
    match = re.search(r"session=([^;]+)", cookie_header)
    return match.group(1) if match else None


def print_response(response):
    """
    Debug printer for HTTP responses.
    """
    print(f"\n[{response.request.method}] {response.url}")
    print(f"Status: {response.status_code}")
    try:
        print("Response JSON:", json.dumps(response.json(), indent=2))
    except Exception:
        print("Response Text:", response.text[:300])
    print("-" * 60)


def assert_json_ok(response):
    """
    Helper assertion for {"ok": True}
    """
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    assert response.json().get("ok") is True, f"Response not ok: {response.text}"


# -----------------------------------------------------
# General HTTP helpers — EACH uses a new session
# -----------------------------------------------------
def get(path: str, headers=None, cookies=None):
    s = new_session()
    return s.get(f"{BASE_URL}{path}", headers=headers, cookies=cookies)


def post(path: str, data=None, json=None, headers=None, files=None, cookies=None):
    s = new_session()
    return s.post(f"{BASE_URL}{path}", data=data, json=json, headers=headers, files=files, cookies=cookies)


# -----------------------------------------------------
# Webpage & Auth Endpoints
# -----------------------------------------------------
def check_get_webpage(path="/"):
    response = get(path)
    print_response(response)
    return response


def check_register_user(username, password, password_confirmation):
    payload = {
        "username": username,
        "password": password,
        "password_confirmation": password_confirmation
    }
    response = post("/register", json=payload)
    print_response(response)
    return response


def check_login_user(username, password):
    payload = {"username": username, "password": password}
    response = post("/login", json=payload)
    print_response(response)
    return response


def check_logout_user(cookie):
    response = get("/logout", cookies={"session": cookie})
    print_response(response)
    return response


def check_dashboard(cookie):
    response = get("/dashboard", cookies={"session": cookie})
    print_response(response)
    return response


# -----------------------------------------------------
# Domain Management
# -----------------------------------------------------
def add_domain(domain, cookie):
    headers = {"Content-Type": "application/json"}
    payload = {"domain": domain}
    response = post("/add_domain", json=payload, headers=headers, cookies={"session": cookie})
    print_response(response)
    return response


def remove_domains(domains, cookie):
    headers = {"Content-Type": "application/json"}
    payload = {"domains": domains}
    response = post("/remove_domains", json=payload, headers=headers, cookies={"session": cookie})
    print_response(response)
    return response


def list_domains(cookie):
    response = get("/my_domains", cookies={"session": cookie})
    print_response(response)
    return response


def bulk_upload_domains(file_path, cookie):
    with open(file_path, "rb") as f:
        response = post("/bulk_domains", files={"file": f}, cookies={"session": cookie})
    print_response(response)
    return response


# -----------------------------------------------------
# Domain Monitoring
# -----------------------------------------------------
def check_scan_domains(session_cookie=None):
    cookies = {"session": session_cookie} if session_cookie else None
    response = get("/scan_domains", cookies=cookies)
    print_response(response)
    return response


# -----------------------------------------------------
# Remove user from app state
# -----------------------------------------------------
def remove_user_from_running_app(username):
    get("/logout")
    UM().remove_user(username)
    result = get("/reload_users_to_memory")
    return result
