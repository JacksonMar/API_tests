import requests
from tests.data import Pets
from pathlib import Path


class PETS:
    BASE_URL = "https://petstore.swagger.io/v2/"
    headers = {
        'Content-Type': 'application/json'
    }

    def add_pet_to_store(self):
        url = self.BASE_URL + "pet/"
        response = requests.post(url, headers=self.headers, json=Pets.pet.value)
        return response

    def get_pet(self, pet_id):
        url = self.BASE_URL + "pet/" + str(pet_id)
        response = requests.get(url, headers=self.headers)
        return response

    def filter_pet_by_status(self, status):
        url = self.BASE_URL + "pet/" + "findByStatus?status=" + status
        response = requests.get(url, self.headers)
        return response

    def add_image_to_pet(self):
        url = self.BASE_URL + "pet/228/uploadImage"
        headers = {
            'accept': 'application/json'
        }
        project_root = Path(__file__).parent.parent
        file_path = project_root / 'Screenshot.png'
        files = {"file": (file_path.name, file_path.open('rb'), 'image/png')}
        data = {"additionalMetadata": "some_date"}
        response = requests.post(url, headers=headers, files=files, data=data)
        return response

    def delete_pet(self, id):
        url = self.BASE_URL + "pet/" + str(id)
        response = requests.delete(url, headers=self.headers)
        return response

    def update_pet(self, pet_date):
        url = self.BASE_URL + "pet/"
        response = requests.put(url, headers=self.headers, json=pet_date)
        return response