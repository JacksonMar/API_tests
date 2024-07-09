# API Tests Project

## Description
This project contains automated tests for APIs using `pytest` and `playwright`.

## Requirements
- Python 3.12
- Docker

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/JacksonMar/API_tests.git
    cd API_tests
    ```
2. Create venv
   ```sh
   python3 -m venv .venv
   ```
   ```sh
   source .venv/bin/activate
   ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
### Running Tests Locally
To run the tests locally, execute the following command:
```sh
pytest . -s -v --html=report.html
```


### Running Tests in Docker
```sh
docker build -t my-test-image .
```
```sh
docker run -v $(pwd):/API_tests my-test-image
```

