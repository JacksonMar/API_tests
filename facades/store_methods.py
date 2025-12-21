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
        return response

    def get_order(self, id):
        url = self.BASE_URL + "store/order/" + str(id)
        response = requests.get(url, headers=self.headers)
        return response

    def inventory_orders(self):
        url = self.BASE_URL + "store/inventory"
        response = requests.get(url, headers=self.headers)
        return response

    def delete_order(self, id):
        url = self.BASE_URL + "store/order/" + str(id)
        response = requests.delete(url, headers=self.headers)
        return response