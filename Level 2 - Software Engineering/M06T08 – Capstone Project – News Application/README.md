# News Application - Open and Check Articles (Windows, MariaDB)

This guide is for a new user who only wants to run the app and verify articles in the browser.

## 1. Required tools

Make sure these are already installed on your machine:

- Git
- Python 3.12+
- MariaDB Server

## 2. Clone the repository

```powershell
git clone https://github.com/nathankap/Capstone-Project---News-Application.git
cd "M06T08 – Capstone Project – News Application"
```

## 3. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If script execution is blocked, run this once, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 4. Install Python dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Start MariaDB service

Try this first:

```powershell
Get-Service | Where-Object { $_.Name -like "MariaDB*" }
Start-Service MariaDB
```

If service name is different, use the exact Name shown by the first command.

## 6. Open MariaDB shell

If mariadb works from PATH:

```powershell
mariadb -u root -p
```

If mariadb is not recognized, use this:

```powershell
& "C:\Program Files\MariaDB 12.3\bin\mariadb.exe" -u root -p
```

Enter your MariaDB root password when prompted.

## 7. Create database and app user

Inside MariaDB shell, paste all lines below:

```sql
CREATE DATABASE news_app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'news_user'@'localhost' IDENTIFIED BY 'news_password';
GRANT ALL PRIVILEGES ON news_app_db.* TO 'news_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 8. Set DB environment variables in this PowerShell session

Run these in the same PowerShell window where your venv is active:

```powershell
$env:DB_NAME="news_app_db"
$env:DB_USER="news_user"
$env:DB_PASSWORD="news_password"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

Important: if you open a new terminal later, set these again.

## 9. Run migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

## 10. Create users for quick article check

Create one editor and one journalist:

```powershell
python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.create_user(username='editor1', password='Password123!', role='editor', role_approved=True); U.objects.create_user(username='journalist1', password='Password123!', role='journalist', role_approved=True); print('Users created')"
```

If users already exist, you can skip this step.

## 11. Start server

```powershell
python manage.py runserver 127.0.0.1:8000
```

Keep this terminal open while testing.

## 12. Check article flow in browser

1. Open http://127.0.0.1:8000/
2. Click Login.
3. Login as journalist1 / Password123!
4. Open Dashboard.
5. Click Create Article.
6. Enter title and content, submit.
7. Logout.
8. Login as editor1 / Password123!
9. Open Dashboard.
10. Click Review Pending Articles.
11. Approve the article.
12. Go to Home and click the article title to open full article page.

You have now verified article creation, approval, and viewing.

## 13. Common fixes

### "python is not recognized"

Close terminal, open a new PowerShell, run:

```powershell
python --version
```

If still missing, reinstall Python and restart Windows.

### "mariadb is not recognized"

Use full path command:

```powershell
& "C:\Program Files\MariaDB 12.3\bin\mariadb.exe" -u root -p
```

### App cannot connect to DB

1. Confirm MariaDB service is running.
2. Re-run environment variable commands in step 8.
3. Re-run migrations.

### Port already in use

Run server on another port:

```powershell
python manage.py runserver 127.0.0.1:8001
```
