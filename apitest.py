import requests

def test_get_webpage():
    response = requests.get("http://localhost:8080/")
    if response.status_code == 200:
        return True
    else:
        return False
    
def test_register_user(name, password):
    url = "http://localhost:8080/register"
    payload = {
        "username": name,
        "password": password,
        "password_confirmation": password
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Status Code:", response.status_code)
    print("Response:", response.text)


print (f"Get webpage: {test_get_webpage()}")
register_result = test_register_user("testuser", "Testpass123")
print (f"Register user result: {register_result}")