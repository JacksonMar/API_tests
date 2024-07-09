from datetime import datetime, timedelta
from enum import Enum, auto


class User(Enum):
    USER_TEST_DATA = {
        "id": 69,
        "username": "Jeckson",
        "firstName": "Jeckson",
        "lastName": "Mar",
        "email": "test@test.ua",
        "password": "12345",
        "phone": "+380663333333",
        "userStatus": 0
    }

    USER_Barsik_DATA = {
        "id": 8100,
        "username": "Barsik",
        "firstName": "Jeckson",
        "lastName": "Cat",
        "email": "barsik@test.ua",
        "password": "12345",
        "phone": "+380663333333",
        "userStatus": 0
    }

class Pets(Enum):

    pet = {
          "id": 228,
          "category": {
            "id": 81,
            "name": "Cats"
          },
          "name": "Barsik",
          "photoUrls": [
            "https://cdn.britannica.com/25/172925-050-DC7E2298/black-cat-back.jpg"
          ],
          "tags": [
            {
              "id": 1,
              "name": "cats"
            }
          ],
          "status": "sold"
        }

    PETS_STATUS = {
        1: "available",
        2: "pending",
        3: "sold"
    }

    update_pet = {
            "id": 228,
            "category": {
                "id": 1,
                "name": "Cats"
            },
            "name": "Big-Bara-Bum",
            "photoUrls": [
                "https://cdn.britannica.com/25/172925-050-DC7E2298/black-cat-back.jpg",
                "https://cdn.britannica.com/34/235834-050-C5843610/two-different-breeds-of-cats-side-by-side-outdoors-in-the-garden.jpg"
            ],
            "tags": [
                {
                    "id": 1,
                    "name": "cats"
                },
                {"id": 7,
                 "hash": "@zanzare"}
            ],
            "status": "available"
        }

class Orders(Enum):
    @staticmethod
    def time_delivery():
        current_date = datetime.utcnow()
        new_date = current_date + timedelta(days=3)
        new_date_iso = new_date.isoformat()
        return new_date_iso

    DATA_ORDER = {
          "id": 9,
          "petId": 228,
          "quantity": 10,
          "shipDate": time_delivery(),
          "status": "available",
          "complete": True
        }

