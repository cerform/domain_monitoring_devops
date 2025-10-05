import socket
import ssl
import concurrent.futures
from datetime import datetime, timezone
from typing import Dict, Any, List
from logger import setup_logger
from DomainManagementEngine import DomainManagementEngine

logger = setup_logger("MonitoringSystem")


class MonitoringSystem:
    @staticmethod
    def _check_domain(domain: str) -> Dict[str, Any]:
        """
        Check reachability and SSL certificate details using sockets.
        """
        result = {
            "domain": domain,
            "status": "Unreachable",
            "ssl_expiration": "N/A",
            "ssl_issuer": "N/A"
        }

        host = domain.lower().strip()
        if host.startswith("http://"):
            host = host[7:]
        elif host.startswith("https://"):
            host = host[8:]
        host = host.split("/")[0]

        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((host, 443), timeout=6) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()

                    expiry_str = cert.get("notAfter")
                    if expiry_str:
                        expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
                        expiry_date = expiry_date.replace(tzinfo=timezone.utc)
                        result["ssl_expiration"] = expiry_date.isoformat()

                        if expiry_date < datetime.now(timezone.utc):
                            result["status"] = "Expired SSL"
                        else:
                            result["status"] = "Active"

                    issuer = next(
                        (v for tup in cert.get("issuer", []) for k, v in tup if k == "organizationName"),
                        None
                    )
                    result["ssl_issuer"] = issuer or "Unknown"

        except socket.timeout:
            result["status"] = "Timeout"
            logger.warning(f"Timeout while checking {domain}")
        except ssl.SSLError:
            result["status"] = "SSL Error"
        except Exception as e:
            logger.warning(f"Error checking {domain}: {e}")

        return result

    @staticmethod
    def scan_user_domains(username: str, max_workers: int = 10) -> List[Dict[str, Any]]:
        """
        Run SSL and reachability checks for all domains of a user concurrently.
        """
        dme = DomainManagementEngine()
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
