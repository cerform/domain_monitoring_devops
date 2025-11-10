import Aux_Library
import sys
import os
import pytest

def test_scan_domains_before_login():

    """
    checking that the endpoint is not reachable without login

    """
    response = Aux_Library.check_scan_domains(session_cookie="")
    assert response.status_code in (401,403,302)

def test_scan_domains_after_login():





# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from app import app
