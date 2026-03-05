import pytest
from tests import data


@pytest.mark.usefixtures("api")
class TestPets:
    UPDATE_PET = None

    @pytest.mark.high
    @pytest.mark.medium
    def test_create_pet(self, api, time_response):
        response = api.pet.add_pet_to_store()
        assert response.status_code == 200

    @pytest.mark.high
    def test_get_pet(self, api, time_response):
        id = data.Pets.pet.value.get("id")
        response = api.pet.get_pet(str(id))
        assert response.status_code == 200
        pet = response.json()
        assert pet.get("name") == "Barsik"

    @pytest.mark.medium
    @pytest.mark.parametrize("param, type", [
        ("id", int),
        ("category", dict),
        ("name", str),
        ("photoUrls", list),
        ("tags", list),
        ("status", str)
    ])
    def test_check_type_value(self, api, time_response, param, type):
        response = api.pet.get_pet(data.Pets.pet.value.get("id"))
        assert response.status_code == 200
        pet = response.json()
        assert isinstance(pet.get(param), type)

    @pytest.mark.low
    def test_filter_pet_by_status(self, api, time_response):
        response = api.pet.filter_pet_by_status(data.Pets.PETS_STATUS.value.get(1))
        assert response.status_code == 200
        list_pets = response.json()
        assert len(list_pets) > 0
        found = False
        for pet in list_pets:
            if pet.get("id") == 228:
                assert pet.get("name") == "Barsik"
                found = True
                break
        if not found:
            pytest.skip("Pet with id 228 not found in available pets")

    @pytest.mark.medium
    def test_upload_image(self, api):
        response = api.pet.add_image_to_pet()
        assert response.status_code == 200
        result = response.json()
        assert "some_date" in result.get("message") and "Screenshot.png" in result.get("message")

    @pytest.mark.medium
    def test_update_pet(self, api, time_response):
        response = api.pet.update_pet(data.Pets.update_pet.value)
        assert response.status_code == 200
        TestPets.UPDATE_PET = response.json()
        print(TestPets.UPDATE_PET)

    @pytest.mark.medium
    @pytest.mark.parametrize("key",[
        ("name"),
        ("category"),
        ("photoUrls"),
        ("tags"),
        ("status")
    ])
    def test_check_update_pet(self, api, time_response, key):
        print(TestPets.UPDATE_PET.get(key))
        assert TestPets.UPDATE_PET.get(key) != data.Pets.pet.value.get(key)

    @pytest.mark.high
    def test_delete_pet(self, api, time_response):
        response = api.pet.delete_pet(data.Pets.pet.value.get("id"))
        assert response.status_code == 200

    @pytest.mark.high
    def test_check_deleted_pet(self, api, time_response):
        id = data.Pets.pet.value.get("id")
        response = api.pet.get_pet(str(id))
        assert response.status_code == 404
        deleted_pet = response.json()
        assert "Pet not found" in deleted_pet.get("message")
        print(deleted_pet)

    @pytest.mark.medium
    def test_check_status_in_deleted_pet(self, api, time_response):
        response = api.pet.get_pet(str(data.Pets.pet.value.get("id")))
        assert response.status_code == 404
        deleted_pet = response.json()
        assert deleted_pet.get("code") == 1





