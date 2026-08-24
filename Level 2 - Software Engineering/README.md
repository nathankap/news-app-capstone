# News App Capstone (M06T08)

This README explains how to build and run the Django News App with either a Python virtual environment or Docker.

Project path:
- M06T08 – Capstone Project – News Application

## Run with venv

1. Open PowerShell and go to the project folder:

```powershell
cd "Level 2 - Software Engineering/M06T08 – Capstone Project – News Application"
```

2. Create and activate venv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Set database environment variables (example values):

```powershell
$env:DB_NAME="news_app_db"
$env:DB_USER="news_user"
$env:DB_PASSWORD="your_password_here"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

5. Apply migrations and run server:

```powershell
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

6. Open:
- http://127.0.0.1:8000

## Run with Docker

1. From the same project folder, build image:

```powershell
docker build -t news-app:latest .
```

2. Run container:

```powershell
docker run --rm -p 8000:8000 news-app:latest
```

3. Open:
- http://127.0.0.1:8000

## Secrets and credentials

Do not commit real passwords, access tokens, or secret keys.
Use local environment variables or your own secret manager.
