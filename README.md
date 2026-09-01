# API Tests

[![tests](https://github.com/JacksonMar/API_tests/actions/workflows/tests.yml/badge.svg)](https://github.com/JacksonMar/API_tests/actions/workflows/tests.yml)

REST API tests for the [Swagger Petstore](https://petstore.swagger.io/v2/) demo service — the `pet`,
`store` and `user` resources. 59 tests with `pytest` + `requests`: 44 happy-path checks and 15
negative cases (missing entities, invalid payloads, wrong credentials). HTTP calls live in facade
classes under `facades/`, so tests only assert.

## Requirements
- Python 3.12
- Docker (optional, for containerised runs)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/JacksonMar/API_tests.git
    cd API_tests
    ```
2. Create and activate a virtualenv:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
### Running tests locally
```sh
pytest -v --html=report.html
```

Tests are tagged by priority, so a subset can be run on its own:
```sh
pytest -m high -v
```
Available markers: `high`, `medium`, `low`.

### Running tests in Docker
```sh
docker build -t my-test-image .
docker run -v $(pwd):/app my-test-image
```

## Project structure
```
facades/   API clients — one class per Petstore resource (store, users, pets)
tests/     Test suites, shared fixtures (conftest.py) and test data (data.py)
```

## Known limitations
- Tests run against the public Petstore sandbox, whose data is shared and periodically reset, so a
  failure may reflect the state of the environment rather than a regression.
- Some suites share class-level state (for example `TestStore.ORDER_ID`) and therefore depend on
  execution order; they are not yet safe to run individually or in parallel.
- Test data is hardcoded in `tests/data.py` rather than generated per run, which can cause
  collisions when the suite runs concurrently.
- Responses are checked field by field; there is no JSON schema validation yet.
