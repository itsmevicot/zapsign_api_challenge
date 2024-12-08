
# ZapSign Backend Challenge

This project is an API built with Django Rest Framework and it's the backend for the ZapSign challenge.

The API is responsible for managing companies, documents, and signers. It includes features like company registration, token-based authentication, document creation, signature requests, and document signing.

It also makes requests to the [ZapSign Sandbox API](https://sandbox.app.zapsign.com.br/) to create documents and signers.

## Overview

This project demonstrates the following features:
- Integration with the Sandbox API of ZapSign.
- Token-based authentication.
- Swagger and Redoc documentation.


## Prerequisites

- Python >= 3.10
- Docker and Docker Compose (optional for containerized deployment)
- PostgreSQL (or Dockerized equivalent)
- [Postman](https://www.postman.com/downloads/) (optional for testing)

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/itsmevicot/zapsign_api_challenge.git
   cd zapsign_api_challenge
   ```

2. **Optional**: Create a virtual environment and activate it:
   - Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the provided `.env.example`.

5. Generate a secure `SECRET_KEY`:
   ```bash
   python manage.py shell
   from django.core.management.utils import get_random_secret_key
   get_random_secret_key()
   ```

6. Run the application:
   - With Docker:
     ```bash
     docker-compose up -d --build
     ```
   - Without Docker:
     ```bash
     python manage.py runserver
     ```

7. Access the project at [http://localhost:8000](http://localhost:8000).

8. You can load a fixture into the database to have some initial dump data:
   ```bash
   python manage.py loaddata fixtures/dump_data.json
   ```
**IMPORTANT**: This data is only for showcasing purposes since they were created without communicating with the ZapSign Sandbox API.


## Technologies Used

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **Deployment**: Docker, Docker Compose
- **Testing**: Pytest

## Architecture

This project follows a layered architecture:
- `views.py`: Handles incoming HTTP requests and returns responses.
- `serializers.py`: Manages data serialization, deserialization, and validation.
- `services.py`: Contains business logic.
- `repositories.py`: Manages database queries.
- `models.py`: Defines database schemas.

## Testing

Run tests using Pytest:
```bash
pytest
```
To test specific modules:
```bash
pytest <module_path>
```
Example:
```bash
pytest unit_tests/authentication
```

Also, you can check the test coverage by running:
```bash
pytest --cov=. --cov-report=term-missing
```

## API Documentation

Access Swagger and Redoc documentation at:
- [Swagger UI](http://localhost:8000/docs)
- [Redoc](http://localhost:8000/redoc)

## Postman API Collection

A [Postman API collection](zapsign-backend.postman_collection.json) is included for easier testing. Import the collection and configure the token as an environment variable.
