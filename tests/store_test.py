from random import randrange

import pytest

from tests.data import Orders as DO

from tests import data


class TestStore:
    INVENTORY = {}
    ORDER_ID = None

    @pytest.mark.high
    def test_create_order(self, api, time_response):
        data_order = DO.DATA_ORDER.value
        response = api.store.ordering(data_order)
        assert response.status_code == 200
        order = response.json()
        assert order.get("id") <= 10

    @pytest.mark.medium
    def test_get_order(self, api, time_response):
        response = api.store.get_order(data.Orders.DATA_ORDER.value.get("id"))
        assert response.status_code == 200
        order_info = response.json()
        assert order_info.get("petId") == 228

    @pytest.mark.low
    def test_get_inventory_orders(self, api, time_response):
        response = api.store.inventory_orders()
        assert response.status_code == 200
        self.INVENTORY.update(response.json())
        assert isinstance(self.INVENTORY.get("available"), int)

    @pytest.mark.high
    def test_create_sold_order(self, api, time_response):
        date_order = data.Orders.DATA_ORDER.value.copy()
        date_order["status"] = "sold"
        # kept clear of the 1-10 range the other order tests write to
        TestStore.ORDER_ID = randrange(1000, 10000)
        date_order["id"] = TestStore.ORDER_ID
        response = api.store.ordering(date_order)
        assert response.status_code == 200

        # the inventory counters are global to the shared sandbox and move
        # under other clients, so the order itself is what gets asserted
        response = api.store.get_order(TestStore.ORDER_ID)
        assert response.status_code == 200
        order = response.json()
        assert order.get("id") == TestStore.ORDER_ID
        assert order.get("status") == "sold"

    @pytest.mark.high
    def test_delete_order(self, api, time_response):
        response = api.store.delete_order(TestStore.ORDER_ID)
        assert response.status_code == 200
        assert response.headers.get("server") == "Jetty(9.2.9.v20150224)"
        assert response.json().get("message") == str(TestStore.ORDER_ID)

    @pytest.mark.high
    @pytest.mark.medium
    def test_check_deleted_order(self, api, time_response):
        response = api.store.get_order(TestStore.ORDER_ID)
        assert response.status_code == 404
        assert "not found" in response.json().get("message", "").lower()

    @pytest.mark.low
    @pytest.mark.parametrize("param, value",[
        ("id", int),
        ("petId", int),
        ("quantity", int),
        ("shipDate", str),
        ("status", str),
        ("complete", bool)
    ])
    def test_check_types_order(self, api, time_response, param, value):
        order_id = data.Orders.DATA_ORDER.value.get("id")
        response = api.store.get_order(order_id)
        if response.status_code == 200:
            order = response.json()
            assert isinstance(order.get(param), value)
        else:
            pytest.skip(f"Order {order_id} not found")





