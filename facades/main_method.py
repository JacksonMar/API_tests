from facades.pets_methods import PETS
from facades.store_methods import STORE
from facades.users_methods import USER


class API:

    BASE_URL = "https://petstore.swagger.io/v2/"
    headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.user = USER()
        self.store = STORE()
        self.pet = PETS()

