## Overview

BlogAPI is a modern, feature-rich backend API for a blogging platform built using FastAPI. It is designed for asynchronous operations, scalability, and ease of development. The project integrates powerful tools for email sending, AI-generated images, cloud storage, and logging. This guide walks you through setting up, running, and testing the API.

### Features

- FastAPI for high-performance asynchronous API development.
- SQLAlchemy and asyncpg for database interactions.
- Email sending via Mailgun.
- AI-generated images powered by DeepAI.
- Cloud storage integration with Backblaze B2.
- Detailed logging using Logtail.
- Secure authentication with python-jose and passlib.
- Full support for asynchronous file handling.

### Setup Instructions

1. Environment Setup

<!-- set the Python version locally -->

```bash
pyenv local 3.11

```

<!-- Check python version  -->

```bash
pyenv exec python -v

```

<!--  create and activate a virtual environment: -->

```bash
pyenv exec python -m venv .venv
python3 -m venv .venv
source .venv/bin/activate

```

2. Installing Dependencies

```bash
pip install -r requirements.txt  # Core dependencies
pip install -r requirements-dev.txt  # Development dependencies

```

<!-- To set up development mode: -->

```bash
    python3 -m pip install -e .
    python3 -m pip install -e . --no-deps
```

<!--  Upgrade requirements -->

```bash
pip install --upgrade -r requirements.txt

```

3. Running the Application

```bash
    uvicorn blogapi.main:app --reload
```

- The API will be live and ready to handle requests at http://127.0.0.1:8000.

### Development and Testing

<!-- Install and activate the dev environment: -->

```bash
    hatch env create dev
    hatch shell dev
```

 <!-- Verify Installation -->

```bash
    pip freeze
```

<!-- To run test -->

```bash
    pytest
    pytest -k <test_name>
    pytest --fixtures
    pytest --fixtures-per-test
```
