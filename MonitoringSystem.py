import socket
import ssl
import concurrent.futures
from datetime import datetime, timezone
from typing import Dict, Any, List
import requests
from logger import setup_logger
from DomainManagementEngine import DomainManagementEngine

logger = setup_logger("MonitoringSystem")

SSL_CTX = ssl.create_default_context()

class MonitoringSystem:
    @staticmethod
    def _check_domain(domain: str) -> Dict[str, Any]:
        """
        Check reachability and SSL certificate details using sockets.
        Falls back to HTTP port 80 if SSL is unavailable.
        Returns: Live / Expired SSL / Down
        """
        result = {
            "domain": domain,
            "status": "Down",
            "ssl_expiration": "N/A",
            "ssl_issuer": "N/A"
        }

        # Normalize host
        host = domain.lower().strip().replace("http://", "").replace("https://", "").split("/")[0]

        # --- Try HTTPS first ---
        try:
            with socket.create_connection((host, 443), timeout=1) as sock:
                with SSL_CTX.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()

                    expiry_str = cert.get("notAfter")
                    if expiry_str:
                        expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z").replace(
                            tzinfo=timezone.utc
                        )
                        result["ssl_expiration"] = expiry_date.strftime("%Y-%m-%d")

                        result["status"] = "Live"

                    issuer = next(
                        (v for tup in cert.get("issuer", []) for k, v in tup if k == "organizationName"),
                        None
                    )
                    result["ssl_issuer"] = issuer or "Unknown"

            return result 

        except (socket.gaierror, socket.timeout, ssl.SSLError, socket.error) as e:
            logger.warning(f"HTTPS failed for {domain}: {e}")

        # --- Fallback: try HTTP port 80 ---
        try:   
            with socket.create_connection((host, 80), timeout=1) as sock:
                http_request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                sock.sendall(http_request.encode())
                response = sock.recv(512).decode(errors="ignore")

                if "HTTP" in response:
                    result["status"] = "Live"
                else:
                    result["status"] = "Down"

        except socket.timeout:
            logger.warning(f"Timeout while checking HTTP for {domain}")
        except Exception as e:
            logger.warning(f"HTTP fallback failed for {domain}: {e}")

        return result


    @staticmethod
    def scan_user_domains(username: str, dme: DomainManagementEngine, max_workers: int = 20) -> List[Dict[str, Any]]:
        """
        Run SSL and reachability checks for all domains concurrently.
        """
        domains = dme.load_user_domains(username)
        if not domains:
            return []

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(MonitoringSystem._check_domain, d["domain"]): d for d in domains}
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f"Domain check failed in worker: {e}")

        dme.save_user_domains(username, results)
        logger.info(f"{len(results)} domains scanned for {username}")
        return results
