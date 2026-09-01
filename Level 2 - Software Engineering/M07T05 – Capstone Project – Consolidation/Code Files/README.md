# News Application

A modular Django web application and REST API for publishing news articles and newsletters with role-based access control (Readers, Journalists, Editors).

## Features

- **Custom User Roles**: Readers, Journalists, and Editors.
- **Article & Newsletter Management**: Creation, viewing, approval workflows, and subscriptions.
- **REST API Endpoints**: Authentication, article feeds, subscription filtering, and newsletter endpoints.
- **Automated Testing & Sphinx Documentation**: Full test coverage and auto-generated Sphinx docs.
- **Containerised Deployment**: Single container Dockerfile & multi-container Docker Compose setup with MariaDB.

---

## Prerequisites

- Python 3.12+ (for local venv setup)
- Docker & Docker Compose (for containerised deployment)

---

## 1. Local Setup with Virtual Environment (venv)

### Step 1: Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Environment Variables & Database Configuration

By default, the application runs on SQLite (`db.sqlite3`). To connect to a MariaDB/MySQL database server, set the following environment variables on your system:

- `DB_NAME`: Database name (e.g., `newsdb`)
- `DB_USER`: Database user (e.g., `newsuser`)
- `DB_PASSWORD`: Database user password
- `DB_HOST`: Database server hostname or IP address (e.g., `localhost` or `db`)
- `DB_PORT`: Database port (default: `3306`)

> **Security Note:** Never commit database passwords, API keys, or secret tokens directly to a repository. Store credentials in environment variables or a local `.env` file excluded by `.gitignore`.

### Step 4: Run Migrations

```bash
python manage.py migrate
```

### Step 5: Start Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 2. Containerised Setup with Docker & Docker Compose

### Option A: Multi-Container Setup using Docker Compose (Recommended)

Docker Compose automatically sets up both the **Django Web Application** container and a **MariaDB Database** container (`db` host) with automatic networking and health checks.

#### Start Application Stack:
```bash
docker-compose up --build
```

- The Django app will automatically run database migrations on startup and launch at `http://127.0.0.1:8000/`.
- MariaDB will run on port `3306` inside the `db` service.

#### Stop Application Stack:
```bash
docker-compose down
```

#### Stop Stack and Remove Data Volumes:
```bash
docker-compose down -v
```

---

### Option B: Standalone Docker Image

To build and run the Django application image directly (using default SQLite storage):

#### Build Image:
```bash
docker build -t news-app:latest .
```

#### Run Container:
```bash
docker run --rm -p 8000:8000 news-app:latest
```

Open `http://127.0.0.1:8000/` in your browser.

---

## 3. Sphinx Documentation

Generated documentation is located in the `docs/` folder.

To rebuild the Sphinx documentation locally:

```bash
cd docs
.\make.bat html
```

Or using `sphinx-build`:

```bash
python -m sphinx -b html docs/source docs/build/html
```

View the documentation by opening `docs/build/html/index.html` or `docs/_build/html/index.html` in your web browser.

---

## 4. Running Automated Tests

Run the Django test suite to verify application endpoints and role permissions:

```bash
python manage.py test news_app
```
