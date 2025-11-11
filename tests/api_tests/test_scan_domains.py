import Aux_Library
import sys
import os
import pytest
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app

def test_scan_domains_unauthorized():

    """
    Calls /scan_domains with NO session cookie.
    Expected: 
    -401 Unauthorized 
    -JSON response : {"ok": False, "error": "Unauthorized"}

    """
    response = Aux_Library.check_scan_domains()
    assert response.status_code == 401

    data = response.json()
    assert data.get("ok") is False
    assert data.get("error") == "Unauthorized"

def test_scan_domaians_authorized():
    
    """
    Full flow:
    - register user
    - Login
    - call "scan_domains" with session cookie
    - Check that the response is ok and has an 'update' field.
    """

    username = f"test_scan_user_{uuid.uuid4().hex[:8]}"
    password = "StrongPass123!"

    reg_resp = Aux_Library.check_register_user(
    name=username,
    password=password,
    password_confirmation=password,
                                                )
    assert reg_resp.status_code == 200
