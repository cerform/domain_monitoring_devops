import Aux_Library
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app

def test_scan_domains_unauthorized():

    """
    Calls /scan_domains with NO session cookie.
    Expected: 401 Unauthorized and ok=False with the proper error message.

    """
    response = Aux_Library.check_scan_domains()
    assert response.status_code == 401

    data = response.json()
    assert data.get("ok") is False
    assert data.get("error") == "Unauthorized"





