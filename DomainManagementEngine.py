from __future__ import annotations
import re
from threading import RLock
from typing import Dict, List, Tuple

from UserManagementModule import UserManager

_lock = RLock()


class DomainManagementEngine:


    def __init__(self, user_manager: UserManager | None = None):
        self.um = user_manager or UserManager()

    # ---------------------------
    # Validation
    # ---------------------------
    @staticmethod
    def _normalize(raw: str) -> str:
        """
        Strip scheme, port and path; lower-case the host.
        """
        raw = (raw or "").strip()
        if not raw:
            return ""
        raw = re.sub(r"^https?://", "", raw, flags=re.I)
        host = raw.split("/")[0].split(":")[0]
        return host.lower()

    @staticmethod
    def _is_valid_fqdn(host: str) -> bool:
        """
        Basic FQDN validation covering subdomains; 1–253 total length,
        1–63 per label, letters/digits/hyphen, TLD 2–63 letters.
        """
        if not host:
            return False
        if len(host) > 253:
            return False
        pattern = r"^(?=.{1,253}$)([A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$"
        return re.match(pattern, host) is not None

    def validate_domain(self, raw_domain: str) -> Tuple[bool, str | None, str]:
        """
        Validate and normalize a domain string.
        Returns: (ok, normalized_domain_or_None, reason_if_invalid)
        """
        host = self._normalize(raw_domain)
        if not host:
            return False, None, "empty"

        # If UserManager already has a validator, prefer it:
        if hasattr(self.um, "validate_domain"):
            ok, norm, reason = self.um.validate_domain(host)
            # ensure normalization even if UM returns the same host
            return bool(ok), (norm or host) if ok else None, reason or ("invalid" if not ok else "")

        # Fallback to local validation
        if not self._is_valid_fqdn(host):
            return False, None, "not a valid domain format"
        return True, host, ""

    # ---------------------------
    # Single add / list / remove
    # ---------------------------
    def add_single(self, username: str, raw_domain: str) -> Tuple[bool, Dict]:
        """
        Add a single domain for a user.
        Returns: (ok, result_dict)
          result_dict on success: {"domain": "<normalized>"}
          on failure: {"error": "...", "reason": "..."} (reason optional)
        """
        ok, norm, reason = self.validate_domain(raw_domain)
        if not ok:
            return False, {"error": "Invalid domain", "reason": reason}

        with _lock:
            saved = self.um.add_domain(username, norm)
            if not saved:
                return False, {"error": "Domain already exists"}
            return True, {"domain": norm}

    def list_domains(self, username: str) -> Dict:
        """
        Return current domain JSON structure for a user.
        The structure is whatever UserManager.load_user_domains returns, typically:
        {"domains": [ { "host": "...", ... }, ... ]}
        """
        return self.um.load_user_domains(username)

    def remove_domain(self, username: str, domain: str) -> Tuple[bool, Dict]:
        """
        Optional: remove a domain from user's list.
        Works only if UserManager has save method. If not present, returns False.
        """
        if not hasattr(self.um, "load_user_domains") or not hasattr(self.um, "save_user_domains"):
            return False, {"error": "Removal not supported by current UserManager"}

        norm = self._normalize(domain)
        if not norm:
            return False, {"error": "Invalid domain"}

        with _lock:
            data = self.um.load_user_domains(username)
            before = len(data.get("domains", []))
            data["domains"] = [d for d in data.get("domains", []) if d.get("host") != norm]
            after = len(data.get("domains", []))
            if after == before:
                return False, {"error": "Domain not found"}
            self.um.save_user_domains(username, data)
            return True, {"domain": norm}

    # ---------------------------
    # Bulk add
    # ---------------------------
    def is_txt_filename(self, filename: str) -> bool:
        """
        Simple .txt check for upload gatekeeping.
        """
        return (filename or "").lower().endswith(".txt")

    def bulk_add_from_text(self, username: str, content: str) -> Dict:
        """
        Bulk-validate and add domains from a raw .txt content.
        Returns summary:
        {
          "added": [domain, ...],
          "duplicates": [domain, ...],
          "invalid": [ { "input": "...", "reason": "..." }, ... ]
        }
        """
        added: List[str] = []
        duplicates: List[str] = []
        invalid: List[Dict[str, str]] = []

        lines = (content or "").splitlines()
        for raw in lines:
            raw = (raw or "").strip()
            if not raw:
                continue
            ok, norm, reason = self.validate_domain(raw)
            if not ok or not norm:
                invalid.append({"input": raw, "reason": reason})
                continue
            with _lock:
                saved = self.um.add_domain(username, norm)
                if saved:
                    added.append(norm)
                else:
                    duplicates.append(norm)

        return {"added": added, "duplicates": duplicates, "invalid": invalid}
