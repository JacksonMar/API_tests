import requests
from tests.data import Orders as DO

class STORE:

    BASE_URL = "https://petstore.swagger.io/v2/"
    headers = {
        'Content-Type': 'application/json'
    }

    def ordering(self, date_order):

        url = self.BASE_URL + "store/order"
        response = requests.post(url, headers=self.headers, json=date_order)
        assert response.status_code == 200
        order = response.json()
        return order

    def get_order(self, id):
        url = self.BASE_URL + "store/order/" + str(id)
        assert int(id) <= 10
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        order_info = response.json()
        return order_info

    def inventory_orders(self):
        url = self.BASE_URL + "store/inventory"
        response = requests.get(url, headers=self.headers)
        lisr_inventory = response.json()
        return lisr_inventory

    def delete_order(self, id):
        url = self.BASE_URL + "store/order/" + str(id)
        response = requests.delete(url, headers=self.headers)
        assert response.status_code == 200
        headers = response.headers
        response = response.json()
        return response, headers