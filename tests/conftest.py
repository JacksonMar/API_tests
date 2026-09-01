import time
import uuid
from random import randrange

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


@pytest.fixture
def missing_id():
    """An id that is not present in the Petstore sandbox, fresh for every test.

    The sandbox is shared and its PUT endpoints upsert, so a hardcoded
    "non-existent" id (999999) gets created by one run and then exists for the
    next one. A fresh id per test keeps the negative cases deterministic.
    """
    return randrange(10 ** 12, 10 ** 13)


@pytest.fixture
def missing_username():
    """A username that is not registered in the Petstore sandbox."""
    return "absent_user_" + uuid.uuid4().hex[:12]
