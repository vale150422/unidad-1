import requests

class UserModel:
    BASE = "http://127.0.0.1:8000/api/login/"

    @staticmethod
    def login(username, password):
        data = {"username": username, "password": password}
        response = requests.post(UserModel.BASE, json=data)

        if response.status_code == 200:
            return response.json()
        return None
