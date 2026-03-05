# Звіт з аналізу автотестів API_tests

## Загальна оцінка: 5/10

---

## Позитивні аспекти

### Що реалізовано добре:

1. **Структура проекту** - чітке розділення тестів і фасадів
2. **Система пріоритетів** - використання pytest markers (high, medium, low)
3. **Параметризація** - застосування @pytest.mark.parametrize для перевірки полів
4. **Docker підтримка** - можливість запуску в контейнері
5. **HTML репорти** - інтеграція pytest-html
6. **Фікстури** - використання фікстур для API та вимірювання часу виконання

---

## Критичні проблеми (Блокери)

### 1. Assert'и в Facade методах ❌
**Файли:** `facades/store_methods.py`, `facades/users_methods.py`, `facades/pets_methods.py`

**Проблема:**
```python
# store_methods.py:14-16
response = requests.post(url, headers=self.headers, json=date_order)
assert response.status_code == 200  # ❌ Assert в facade!
order = response.json()
```

**Чому це погано:**
- Порушує принцип єдиної відповідальності (SRP)
- Facade повинен тільки робити запити, не валідувати їх
- Неможливо протестувати негативні сценарії (400, 404, 500)
- Тест падає на рівні facade, а не в самому тесті

**Рекомендація:** Перенести всі assert'и в тести, facade має повертати response objects

---

### 2. Жорстко закодовані дані та ID ❌
**Файли:** `tests/data.py`, `tests/store_test.py`

**Проблема:**
```python
# tests/store_test.py:17-20
def test_create_order(self, api, time_response):
    data_order = DO.DATA_ORDER.value
    order = api.store.ordering(data_order)
    assert order.get("id") <= 10  # ❌ Жорстко закодоване обмеження
```

```python
# tests/data.py:86-91
DATA_ORDER = {
    "id": 9,  # ❌ Фіксоване ID може спричинити конфлікти
    "petId": 228,  # ❌ Жорстка прив'язка до конкретного Pet
    ...
}
```

**Рекомендація:** Використовувати динамічну генерацію даних (faker, factory_boy)

---

### 3. Тести не ізольовані ❌
**Файл:** `tests/store_test.py:33-46`

**Проблема:**
```python
class TestStore:
    INVENTORY = {}  # ❌ Shared state між тестами
    ORDER_ID = None  # ❌ Тести залежать один від одного

    def test_create_sold_order(self, api, time_response):
        TestStore.ORDER_ID = randrange(100)  # Записує ID
        ...

    def test_delete_order(self, api, time_response):
        request, headers = api.store.delete_order(TestStore.ORDER_ID)  # Читає ID
```

**Чому це погано:**
- Порушується принцип ізоляції тестів
- Неможливо запустити один тест окремо
- Непередбачувана поведінка при паралельному запуску

**Рекомендація:** Використовувати фікстури з scope="function" для створення даних

---

### 4. Тест з рандомним ID замість реального ❌
**Файл:** `tests/store_test.py:50-53`

**Проблема:**
```python
@flaky(max_runs=10, min_passes=1)
def test_check_deleted_order(self, api, time_response):
    order = api.store.get_order(randrange(30))  # ❌ Випадковий ID!
    assert order.get("status") == "placed"
```

**Чому це погано:**
- Тест не перевіряє видалений ORDER_ID з попереднього тесту
- Використання @flaky маскує реальну проблему
- Непередбачувана поведінка тесту

**Рекомендація:** Перевірити, що видалений ORDER_ID справді недоступний

---

## Високий пріоритет

### 5. Опечатка в pytest.ini ⚠️
**Файл:** `pytest.ini:5`

```ini
markers =
    high: mark a high priority tests for all projects.
    medium: mark a medium priority tests for all projects.
    lou: mark a lou priority tests for in all project.  # ❌ "lou" → "low"
```

**Виправлення:** Перейменувати "lou" на "low" в pytest.ini та всіх тестах

---

### 6. Опечатка в коді ⚠️
**Файли:**
- `store_methods.py:30` - `lisr_inventory` → `list_inventory`
- `store_test.py:56` - `vale` → `value`
- `users_test.py:40` - `massage` → `message`

---

### 7. Відсутні негативні тести ⚠️

**Проблема:** Всі тести перевіряють тільки "happy path"

**Приклади відсутніх тестів:**
```python
# Чого немає:
- test_create_order_with_invalid_data()      # 400 Bad Request
- test_get_non_existent_order()              # 404 Not Found
- test_create_order_without_auth()           # 401 Unauthorized
- test_delete_already_deleted_order()        # 404 Not Found
- test_create_pet_with_missing_fields()      # 400 Bad Request
- test_update_user_with_duplicate_email()    # 409 Conflict
```

---

### 8. Відсутня валідація JSON схем ⚠️

**Проблема:** Тести перевіряють окремі поля, але не структуру відповіді

**Рекомендація:** Використовувати jsonschema або pydantic models:
```python
from jsonschema import validate

pet_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["available", "pending", "sold"]}
    },
    "required": ["id", "name", "status"]
}

def test_get_pet_schema(api):
    pet = api.pet.get_pet("228")
    validate(instance=pet, schema=pet_schema)
```

---

### 9. Неправильне використання @flaky ⚠️

**Файл:** `tests/store_test.py:50`

```python
@flaky(max_runs=10, min_passes=1)
def test_check_deleted_order(self, api, time_response):
    order = api.store.get_order(randrange(30))
    assert order.get("status") == "placed"
```

**Проблема:**
- @flaky маскує нестабільність тесту
- Тест може проходити випадково (1 з 10 запусків)
- Це не вирішує корінної проблеми

**Рекомендація:** Виправити логіку тесту, а не використовувати retry

---

### 10. Відсутня обробка помилок ⚠️

**Проблема:**
```python
# pets_test.py:36-40
for i in list_pets:
    if i.get("id") == 228:
        assert i.get("name") == "Barsik"
    else:
        assert len(list_pets) > 0  # ❌ Логічно некоректний assert
```

**Рекомендація:**
```python
# Правильний підхід:
found = False
for pet in list_pets:
    if pet.get("id") == 228:
        assert pet.get("name") == "Barsik"
        found = True
        break
assert found, "Pet with id 228 not found"
```

---

## Середній пріоритет

### 11. Дублювання BASE_URL і headers 🔄

**Проблема:** BASE_URL і headers дубльовані в 4 файлах:
- `facades/main_method.py:8-11`
- `facades/store_methods.py:6-9`
- `facades/users_methods.py:7-10`
- `facades/pets_methods.py:7-10`

**Рекомендація:** Винести в окремий config файл або використовувати наслідування

---

### 12. Відсутнє логування 📝

**Рекомендація:** Додати логування для кращої діагностики:
```python
import logging

logger = logging.getLogger(__name__)

def test_create_order(self, api, time_response):
    logger.info("Creating order with data: %s", data_order)
    order = api.store.ordering(data_order)
    logger.info("Order created: %s", order)
    assert order.get("id") <= 10
```

---

### 13. Playwright не використовується 🎭

**Проблема:**
- `requirements.txt` містить playwright
- `Dockerfile` встановлює Chrome і playwright
- Але жоден тест не використовує playwright

**Рекомендація:** Або видалити залежність, або додати UI тести

---

### 14. Відсутні allure репорти 📊

**Рекомендація:** Замість pytest-html використовувати allure для кращої візуалізації:
```bash
pip install allure-pytest
pytest --alluredir=./allure-results
allure serve ./allure-results
```

---

### 15. Немає CI/CD конфігурації ⚙️

**Рекомендація:** Додати GitHub Actions:
```yaml
# .github/workflows/tests.yml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -v --html=report.html
```

---

### 16. Відсутня перевірка статус кодів в тестах 🔍

**Проблема:** Статус коди перевіряються тільки в facades, не в тестах

**Рекомендація:**
```python
def test_create_user(self, api, time_response):
    response = api.user.create_user(User.USER_TEST_DATA.value)
    assert response.status_code == 200  # ✅ Явна перевірка
    assert response.json().get("code") == 200
```

---

### 17. Тестові дані не генеруються динамічно 🎲

**Рекомендація:** Використовувати Faker:
```python
from faker import Faker
fake = Faker()

def generate_user():
    return {
        "id": fake.random_int(min=1000, max=9999),
        "username": fake.user_name(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(),
        "phone": fake.phone_number(),
        "userStatus": 0
    }
```

---

## Низький пріоритет

### 18. Відсутня документація методів 📖

**Рекомендація:** Додати docstrings:
```python
def create_user(self, user_data: dict) -> requests.Response:
    """
    Create a new user in the system.

    Args:
        user_data: Dictionary containing user information

    Returns:
        Response object from the API
    """
    ...
```

---

### 19. Немає type hints 🔤

**Рекомендація:**
```python
from typing import Dict, Any
import requests

def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
    ...
```

---

### 20. Відсутні pre-commit hooks 🪝

**Рекомендація:** Додати `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

---

### 21. Відсутній .gitignore 📁

**Рекомендація:** Створити `.gitignore`:
```
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
report.html
assets/
allure-results/
```

---

## Пріоритизовані рекомендації

### Термінові (виконати першими):

1. **Видалити assert'и з facade методів** - повертати response objects
2. **Виправити test_check_deleted_order** - використовувати ORDER_ID замість randrange
3. **Виправити опечатки** - lou → low, lisr_inventory, vale, massage
4. **Ізолювати тести** - видалити class variables, використовувати фікстури
5. **Додати негативні тести** - мінімум по 2-3 на кожен модуль

### Короткострокові (1-2 тижні):

6. **Додати валідацію JSON схем** - використовувати jsonschema або pydantic
7. **Динамічна генерація даних** - інтегрувати Faker або factory_boy
8. **Винести конфігурацію** - створити config.py для BASE_URL та headers
9. **Додати логування** - для кращої діагностики падінь
10. **Створити .gitignore** - виключити службові файли

### Середньострокові (1 місяць):

11. **Додати CI/CD** - GitHub Actions для автоматичного запуску тестів
12. **Перейти на Allure репорти** - замість pytest-html
13. **Додати type hints** - для всіх методів
14. **Документація** - додати docstrings до всіх методів
15. **Видалити Playwright** - якщо не плануються UI тести

### Довгострокові (за потреби):

16. **Pre-commit hooks** - для перевірки коду перед комітом
17. **Тести продуктивності** - виміряти час відгуку API
18. **Тести безпеки** - перевірити вразливості (SQL injection, XSS)
19. **Паралельний запуск** - pytest-xdist для прискорення
20. **Контрактне тестування** - pact для перевірки контрактів API

---

## Метрики якості

| Метрика | Поточний стан | Ціль |
|---------|--------------|------|
| Покриття тестами | ~60% (тільки happy path) | 90%+ (з негативними тестами) |
| Ізоляція тестів | 40% (є залежності між тестами) | 100% |
| Негативні тести | 0% | 30% від загальної кількості |
| Якість коду (pylint) | ~6/10 | 8+/10 |
| Документація | 10% | 80%+ |
| CI/CD | Немає | Повна автоматизація |

---

## Висновки

### Сильні сторони:
- Добре структурований проект
- Використання pytest та його можливостей
- Docker підтримка
- Система пріоритетів тестів

### Слабкі сторони:
- Assert'и в facade методах (критично)
- Відсутня ізоляція тестів
- Немає негативних тестів
- Жорстко закодовані дані
- Відсутня валідація JSON схем

### Загальна оцінка: 5/10

**Обґрунтування:**
- Базова функціональність працює (+3)
- Хороша структура проекту (+2)
- Критичні помилки в архітектурі (-3)
- Відсутні негативні тести (-2)
- Немає proper isolation (-1)
- Відсутні сучасні практики (allure, CI/CD) (-1)

### Потенціал після виправлень: 8-9/10

При виконанні рекомендацій проект може досягти високого рівня якості та стати хорошим прикладом API тестування.
