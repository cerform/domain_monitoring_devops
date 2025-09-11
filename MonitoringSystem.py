import socket
import ssl
import requests
import concurrent.futures
from datetime import datetime
import threading
import UserManagementModule as UM

# Thread pool size (can be tuned depending on system load)
MAX_WORKERS = 10

# Lock for safe JSON updates
_lock = threading.RLock()


# ---------------------------
# Single domain checks
# ---------------------------
def check_http(domain: str) -> dict:
    """
    Perform a basic HTTP GET request to check if the domain is alive.
    Returns a dict with status code and ok flag.
    """
    url = f"http://{domain}"
    try:
        res = requests.get(url, timeout=5)
        return {"ok": res.status_code == 200, "status": res.status_code}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}


def check_ssl(domain: str) -> dict:
    """
    Connect to domain:443 and fetch SSL certificate information.
    Returns issuer and expiry date if available.
    """
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                exp_str = cert.get("notAfter")
                exp_date = None
                if exp_str:
                    try:
                        exp_date = datetime.strptime(exp_str, "%b %d %H:%M:%S %Y %Z")
                    except Exception:
                        exp_date = exp_str  # keep raw if parsing fails
                return {
                    "ok": True,
                    "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    "expires": exp_date.isoformat() if isinstance(exp_date, datetime) else exp_date,
                }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ---------------------------
# User-level checks
# ---------------------------
def check_domain(domain: str) -> dict:
    """
    Run both HTTP and SSL checks for a domain.
    Returns a unified dict with results.
    """
    http_res = check_http(domain)
    ssl_res = check_ssl(domain)

    return {
        "host": domain,
        "last_check": datetime.utcnow().isoformat() + "Z",
        "http": http_res,
        "ssl": ssl_res,
    }


def check_user_domains(username: str):
    """
    Check all domains for a given user concurrently.
    Updates <username>_domains.json with the latest results.
    """
    data = UM.load_user_domains(username)
    domains = [d.get("host") for d in data.get("domains", [])]

    if not domains:
        return

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_domain = {executor.submit(check_domain, dom): dom for dom in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            results.append(future.result())

    # Update JSON file with results
    with _lock:
        current = UM.load_user_domains(username)
        for res in results:
            for d in current["domains"]:
                if d.get("host") == res["host"]:
                    d.update(res)
        UM.save_user_domains(username, current)


def run_user_check_async(username: str):
    """
    Run user domain check in a background thread.
    Useful for triggering checks via API without blocking request.
    """
    t = threading.Thread(target=check_user_domains, args=(username,), daemon=True)
    t.start()
