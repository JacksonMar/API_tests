import time
import pytest
from facades.main_method import API

@pytest.fixture(scope="session")
def api():
    yield API()


@pytest.fixture(scope="function")
def time_response(request):
    start_time = time.time()

    def fin():
        end_time = time.time()
        duration = end_time - start_time
        if duration <= 2:
            print("  Test {name} took {duration:.2f} seconds".format(name=request.node.name, duration=duration))

    request.addfinalizer(fin)
