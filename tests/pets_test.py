import pytest
from tests import data


@pytest.mark.usefixtures("api")
class TestPets:
    UPDATE_PET = None

    @pytest.mark.high
    @pytest.mark.medium
    def test_create_pet(self, api, time_response):
        api.pet.add_pet_to_store()

    @pytest.mark.high
    def test_get_pet(self, api, time_response):
        id = data.Pets.pet.value.get("id")
        pet = api.pet.get_pet(str(id))
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
        pet = api.pet.get_pet(data.Pets.pet.value.get("id"))
        assert isinstance(pet.get(param), type)

    @pytest.mark.lou
    def test_filter_pet_by_status(self, api, time_response):
        list_pets = api.pet.filter_pet_by_status(data.Pets.PETS_STATUS.value.get(1))
        for i in list_pets:
            if i.get("id") == 228:
                assert i.get("name") == "Barsik"
            else:
                assert len(list_pets) > 0

    @pytest.mark.medium
    def test_upload_image(self, api):
        response = api.pet.add_image_to_pet()
        assert "some_date" in response.get("message") and "Screenshot.png" in response.get("message")

    @pytest.mark.medium
    def test_update_pet(self, api, time_response):
        TestPets.UPDATE_PET = api.pet.update_pet(data.Pets.update_pet.value)
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
        api.pet.delete_pet(data.Pets.pet.value.get("id"))

    @pytest.mark.high
    def test_check_deleted_pet(self, api, time_response):
        id = data.Pets.pet.value.get("id")
        deleted_pet = api.pet.get_pet(str(id))
        assert "Pet not found" in deleted_pet.get("message")
        print(deleted_pet)

    @pytest.mark.medium
    def test_check_status_in_deleted_pet(self, api, time_response):
        deleted_pet = api.pet.get_pet(str(data.Pets.pet.value.get("id")))
        assert deleted_pet.get("code") == 1





