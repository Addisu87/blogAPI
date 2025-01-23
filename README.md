# blogAPI

It is a blog api using fastAPI

<!--  -->

```bash
pyenv local 3.11

```

<!-- Check python version  -->

```bash
pyenv exec python -v

```

<!-- Create a virtual environment -->

```bash
pyenv exec python -m venv .venv
python3 -m venv .venv

```

<!--  To activate virtual environment-->

```bash
source .venv/bin/activate

```

<!-- Install dependencies -->

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt

```

<!-- Working in dev mode -->

```bash
    python3 -m pip install -e .
    python3 -m pip install -e . --no-deps
```

<!--  Upgrade requirements -->

```bash
pip install --upgrade -r requirements.txt

```

<!-- Run Your Application -->

```bash
    uvicorn blogapi.main:app --reload
```

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

<!--  -->

```bash

```

- Mailgun - Email sending platform
- DeepAI - Crate ai-images
- Backblaze/b2sdk - B2 cloud storage
- Logtail - logs for debugging and info
- Aifiles - file support for asyncio
-
