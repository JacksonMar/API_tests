from random import randrange

import pytest
from flaky import flaky
from playwright.sync_api import expect

from tests.data import Orders as DO

from tests import data


class TestStore:
    INVENTORY = {}
    ORDER_ID = None

    @pytest.mark.high
    def test_create_order(self, api, time_response):
        data_order = DO.DATA_ORDER.value
        order = api.store.ordering(data_order)
        assert order.get("id") <= 10

    @pytest.mark.medium
    def test_get_order(self, api, time_response):
        order_info = api.store.get_order(data.Orders.DATA_ORDER.value.get("id"))
        assert order_info.get("petId") == 228

    @pytest.mark.lou
    def test_get_inventory_orders(self, api, time_response):
        self.INVENTORY.update(api.store.inventory_orders())
        assert isinstance(self.INVENTORY.get("available"), int)

    @pytest.mark.high
    def test_create_sold_order(self, api, time_response):
        date_order = data.Orders.DATA_ORDER.value
        date_order["status"] = "sold"
        TestStore.ORDER_ID = randrange(100)
        date_order["id"] = TestStore.ORDER_ID
        api.store.ordering(date_order)
        inventory = api.store.inventory_orders()
        assert inventory.get("sold") == (self.INVENTORY.get("sold"))

    @pytest.mark.high
    def test_delete_order(self, api, time_response):
        request, headers = api.store.delete_order(TestStore.ORDER_ID)
        assert headers.get("server") == "Jetty(9.2.9.v20150224)"
        assert request.get("message") == str(TestStore.ORDER_ID)

    @pytest.mark.high
    @pytest.mark.medium
    @flaky(max_runs=10, min_passes=1)
    def test_check_deleted_order(self, api, time_response):
        order = api.store.get_order(randrange(30))
        assert order.get("status") == "placed"

    @pytest.mark.lou
    @pytest.mark.parametrize("param, vale",[
        ("id", int),
        ("petId", str),
        ("quantity", int),
        ("shipDate", str),
        ("status", str),
        ("complete", bool)
    ])
    def test_check_types_order(self, api, time_response, param, vale):
        order_id = randrange(9)
        try:
            order = api.store.get_order(order_id)
            assert isinstance(order.get(param), vale)
        except AssertionError:
            print(" Order: " + str(order_id) + " nof found")





