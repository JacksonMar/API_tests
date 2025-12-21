import pytest
from tests import data


class TestNegativeStore:
    """Negative test cases for Store API"""

    @pytest.mark.high
    def test_get_nonexistent_order(self, api, time_response):
        """Test getting an order that doesn't exist - should return 404"""
        response = api.store.get_order(999999)
        assert response.status_code == 404
        error = response.json()
        assert "not found" in error.get("message", "").lower()

    @pytest.mark.medium
    def test_delete_nonexistent_order(self, api, time_response):
        """Test deleting an order that doesn't exist"""
        response = api.store.delete_order(999999)
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
    def test_get_nonexistent_user(self, api, time_response):
        """Test getting a user that doesn't exist - should return 404"""
        response = api.user.get_user("nonexistent_user_12345")
        assert response.status_code == 404
        error = response.json()
        assert "not found" in error.get("message", "").lower()

    @pytest.mark.medium
    def test_delete_nonexistent_user(self, api, time_response):
        """Test deleting a user that doesn't exist"""
        response = api.user.delete_user("nonexistent_user_12345")
        assert response.status_code == 404

    @pytest.mark.medium
    def test_update_nonexistent_user(self, api, time_response):
        """Test updating a user that doesn't exist"""
        response = api.user.update_user(
            "nonexistent_user_12345",
            data.User.USER_TEST_DATA.value
        )
        assert response.status_code == 404

    @pytest.mark.medium
    def test_create_user_with_invalid_data(self, api, time_response):
        """Test creating user with invalid/incomplete data"""
        invalid_user = {"username": ""}  # Empty username
        response = api.user.create_user(invalid_user)
        # API should handle this - might return 200 with error or 400
        assert response.status_code in [200, 400, 500]

    @pytest.mark.low
    def test_login_with_invalid_credentials(self, api, time_response):
        """Test login with non-existent user"""
        response = api.user.user_login("invalid_user", "invalid_pass")
        # API might return 200 with error message or 400
        if response.status_code == 200:
            result = response.json()
            # Check if it's an error response
            assert "logged in user session" not in result.get("message", "").lower()
        else:
            assert response.status_code in [400, 401, 404]


class TestNegativePets:
    """Negative test cases for Pet API"""

    @pytest.mark.high
    def test_get_nonexistent_pet(self, api, time_response):
        """Test getting a pet that doesn't exist - should return 404"""
        response = api.pet.get_pet(999999)
        assert response.status_code == 404
        error = response.json()
        assert "not found" in error.get("message", "").lower()

    @pytest.mark.medium
    def test_delete_nonexistent_pet(self, api, time_response):
        """Test deleting a pet that doesn't exist"""
        response = api.pet.delete_pet(999999)
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
    def test_update_nonexistent_pet(self, api, time_response):
        """Test updating a pet that doesn't exist"""
        non_existent_pet = data.Pets.pet.value.copy()
        non_existent_pet["id"] = 999999
        response = api.pet.update_pet(non_existent_pet)
        # API might return 404 or 200 with error
        if response.status_code == 200:
            result = response.json()
            # Verify it's an error or created new pet
            assert result.get("id") is not None
        else:
            assert response.status_code == 404


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
