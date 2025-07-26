import requests

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"

# À adapter selon les utilisateurs trouvés en base
login_data = {
    "username": "coco",
    "password": "coco123"
}

response = requests.post(LOGIN_URL, json=login_data)
print(f"Status: {response.status_code}")
print("Réponse brute:")
print(response.text) 