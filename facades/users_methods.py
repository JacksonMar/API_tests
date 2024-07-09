import json
import requests


class USER:

    BASE_URL = "https://petstore.swagger.io/v2/"
    headers = {
        'Content-Type': 'application/json'
    }

    def create_user(self, user_data):
        url = self.BASE_URL + "user/"
        response = requests.post(url, headers=self.headers, json=user_data)
        assert response.status_code == 200
        return response

    def get_user(self, user_name):
        url = self.BASE_URL + "user/" + user_name
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        return response

    def user_login(self, user_name, user_password):
        url = self.BASE_URL + "user/login?username={user_name}&password={user_password}".format(
            user_name=user_name, user_password=user_password)
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200

        user = response.json()
        message = user.get("message")
        user_session = message.split(":")[1]

        return response, user_session

    def update_user(self, current_name, future_user_data):
        url = self.BASE_URL + "user/" + current_name
        response = requests.put(url, headers=self.headers, json=future_user_data)
        assert response.status_code == 200
        return response

    def user_logout(self):
        url = self.BASE_URL + "user/logout"
        response = requests.get(url, headers=self.headers)
        headers = response.headers
        assert response.status_code == 200
        return response, headers

    def delete_user(self, user_name):
        url = self.BASE_URL + "user/" + user_name
        response = requests.delete(url, headers=self.headers)
        assert response.status_code == 200
        headers = response.headers
        return response, headers





