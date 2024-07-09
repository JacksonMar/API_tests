import pytest
from tests.data import User


class TestUsers:
    USER_JSON = {}
    USER_SESSION = None

    @pytest.mark.high
    def test_user(self, api, time_response):
        user = api.user.create_user(User.USER_TEST_DATA.value)
        assert user.status_code == 200

    @pytest.mark.medium
    @pytest.mark.lou
    def test_get_user(self, api, time_response):
        user_name = User.USER_TEST_DATA.value.get("username")
        user = api.user.get_user(user_name)
        assert user.status_code == 200
        self.USER_JSON.update(user.json())
        assert self.USER_JSON is not None

    @pytest.mark.medium
    @pytest.mark.parametrize("expected_data, data", [
        (User.USER_TEST_DATA.value.get("username"), "username"),
        (User.USER_TEST_DATA.value.get("firstName"), "firstName"),
        (User.USER_TEST_DATA.value.get("lastName"), "lastName"),
        (User.USER_TEST_DATA.value.get("email"), "email"),
        (User.USER_TEST_DATA.value.get("phone"), "phone"),
        (User.USER_TEST_DATA.value.get("userStatus"), "userStatus"),
    ])
    def test_check_fields(self, time_response, api, expected_data, data):
        assert self.USER_JSON.get(data) == expected_data

    @pytest.mark.medium
    def test_user_logining(self, api, time_response):
        user, self.USER_SESSION = api.user.user_login(
            User.USER_TEST_DATA.value.get("username"), User.USER_TEST_DATA.value.get("password"))
        user = user.json()
        massage = user.get("message")
        assert "logged in user session:" in massage

    @pytest.mark.medium
    def test_update_user(self, api, time_response):
        current_name = User.USER_TEST_DATA.value.get("username")
        future_data = User.USER_Barsik_DATA.value
        user = api.user.update_user(current_name, future_data)

    @pytest.mark.medium
    def test_check_barsik_data(self, api, time_response):
        current_user = api.user.get_user(User.USER_Barsik_DATA.value.get("username"))
        barsik = current_user.json()
        assert (barsik.get("username") == User.USER_Barsik_DATA.value.get("username")
                and barsik.get("id") == User.USER_Barsik_DATA.value.get("id")
                and barsik.get("email") == User.USER_Barsik_DATA.value.get("email"))

    @pytest.mark.lou
    def test_logout_user(self, api, time_response):
        response, headers = api.user.user_logout()
        assert "Authorization" in headers.get("access-control-allow-headers")

    @pytest.mark.high
    def test_delete_user(self, api, time_response):
        delete_user, headers = api.user.delete_user(User.USER_TEST_DATA.value.get("username"))
        server = headers.get("Server")
        assert server == "Jetty(9.2.9.v20150224)"


