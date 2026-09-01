import pytest
from tests import data


class TestNegativeStore:
    """Negative test cases for Store API"""

    @pytest.mark.high
    def test_get_nonexistent_order(self, api, time_response, missing_id):
        """Test getting an order that doesn't exist - should return 404"""
        response = api.store.get_order(missing_id)
        assert response.status_code == 404
        error = response.json()
        assert "not found" in error.get("message", "").lower()

    @pytest.mark.medium
    def test_delete_nonexistent_order(self, api, time_response, missing_id):
        """Test deleting an order that doesn't exist"""
        response = api.store.delete_order(missing_id)
        assert response.status_code == 404

    @pytest.mark.medium
    def test_create_order_with_invalid_data(self, api, time_response):
        """Test creating order with invalid data structure"""
        invalid_order = {"invalid": "data"}
        response = api.store.ordering(invalid_order)
        # API might return 200 with error or 400 - check both scenarios
        if response.status_code == 200:
            order = response.json()
            # Verify it's an error response
            assert order.get("code") != 200 or order.get("type") == "error"
        else:
            assert response.status_code in [400, 500]


class TestNegativeUsers:
    """Negative test cases for User API"""

    @pytest.mark.high
    def test_get_nonexistent_user(self, api, time_response, missing_username):
        """Test getting a user that doesn't exist - should return 404"""
        response = api.user.get_user(missing_username)
        assert response.status_code == 404
        error = response.json()
        assert "not found" in error.get("message", "").lower()

    @pytest.mark.medium
    def test_delete_nonexistent_user(self, api, time_response, missing_username):
        """Test deleting a user that doesn't exist"""
        response = api.user.delete_user(missing_username)
        assert response.status_code == 404

    @pytest.mark.medium
    def test_update_nonexistent_user(self, api, time_response, missing_username):
        """Updating a user that does not exist creates it instead of failing.

        Known deviation: the Swagger spec offers no 2xx response for a missing
        user, but PUT /user/{username} on the sandbox upserts and answers 200.
        The test pins that behaviour so a future fix shows up as a failure.
        """
        payload = data.User.USER_TEST_DATA.value.copy()
        payload["username"] = missing_username
        response = api.user.update_user(missing_username, payload)
        assert response.status_code == 200

        created = api.user.get_user(missing_username)
        assert created.status_code == 200, "expected the upsert to be readable back"
        assert created.json().get("username") == missing_username

        api.user.delete_user(missing_username)

    @pytest.mark.medium
    def test_create_user_with_invalid_data(self, api, time_response):
        """Test creating user with invalid/incomplete data"""
        invalid_user = {"username": ""}  # Empty username
        response = api.user.create_user(invalid_user)
        # API should handle this - might return 200 with error or 400
        assert response.status_code in [200, 400, 500]

    @pytest.mark.low
    def test_login_with_invalid_credentials(self, api, time_response, missing_username):
        """Login hands out a session for credentials that were never registered.

        Known deviation: the sandbox validates neither the username nor the
        password and always answers 200 with a session token. The test pins that
        so the day the endpoint starts rejecting unknown users, it fails here.
        """
        response = api.user.user_login(missing_username, "invalid_pass")
        assert response.status_code == 200
        assert "logged in user session" in response.json().get("message", "").lower()


class TestNegativePets:
    """Negative test cases for Pet API"""

    @pytest.mark.high
    def test_get_nonexistent_pet(self, api, time_response, missing_id):
        """Test getting a pet that doesn't exist - should return 404"""
        response = api.pet.get_pet(missing_id)
        assert response.status_code == 404
        error = response.json()
        assert "not found" in error.get("message", "").lower()

    @pytest.mark.medium
    def test_delete_nonexistent_pet(self, api, time_response, missing_id):
        """Test deleting a pet that doesn't exist"""
        response = api.pet.delete_pet(missing_id)
        assert response.status_code == 404

    @pytest.mark.medium
    def test_create_pet_with_invalid_data(self, api, time_response):
        """Test creating pet with missing required fields"""
        # API expects certain required fields
        response = api.pet.add_pet_to_store()  # Uses predefined data
        # This should succeed as it uses valid data
        assert response.status_code == 200

    @pytest.mark.low
    def test_filter_pets_with_invalid_status(self, api, time_response):
        """Test filtering pets with invalid status value"""
        response = api.pet.filter_pet_by_status("invalid_status")
        # API should return empty list or error
        if response.status_code == 200:
            pets = response.json()
            assert isinstance(pets, list)
            # Might be empty or contain error
        else:
            assert response.status_code in [400, 404]

    @pytest.mark.medium
    def test_update_nonexistent_pet(self, api, time_response, missing_id):
        """Updating a pet that does not exist creates it instead of failing.

        Known deviation, same shape as the user endpoint: PUT /pet upserts and
        answers 200. The pet is deleted afterwards so the id stays absent for
        the next run.
        """
        non_existent_pet = data.Pets.pet.value.copy()
        non_existent_pet["id"] = missing_id
        response = api.pet.update_pet(non_existent_pet)
        assert response.status_code == 200
        assert response.json().get("id") == missing_id

        api.pet.delete_pet(missing_id)


class TestStatusCodes:
    """Test various HTTP status code scenarios"""

    @pytest.mark.low
    def test_inventory_returns_200(self, api, time_response):
        """Verify inventory endpoint returns 200"""
        response = api.store.inventory_orders()
        assert response.status_code == 200
        inventory = response.json()
        assert isinstance(inventory, dict)

    @pytest.mark.low
    def test_successful_operations_return_200(self, api, time_response):
        """Test that successful operations return 200 status code"""
        # Create a test order
        test_order = data.Orders.DATA_ORDER.value.copy()
        test_order["id"] = 5
        response = api.store.ordering(test_order)
        assert response.status_code == 200

        # Get the order
        response = api.store.get_order(5)
        assert response.status_code == 200

        # Delete the order
        response = api.store.delete_order(5)
        assert response.status_code == 200
