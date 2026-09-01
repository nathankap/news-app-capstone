# News Application

A Django news application and REST API with role-based access control for readers, journalists, and editors. MariaDB is the default database.

## Local Setup with MariaDB

Prerequisites: Git, Python 3.12+, and a running MariaDB server.

1. Clone the repository and enter the new project folder.

	```powershell
	git clone https://github.com/nathankap/news-app-capstone.git
	cd news-app-capstone
	```

2. Create and activate a virtual environment inside the project folder.

	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

3. Install dependencies.

	```powershell
	pip install -r requirements.txt
	```

4. Create the database and user. Start MariaDB, then sign in as its root user. Enter the root password when prompted.

	```powershell
	mysql -u root -p
	```

	Run the following SQL, replacing both example passwords with secure values:

	```sql
	CREATE DATABASE newsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
	CREATE USER 'newsuser'@'localhost' IDENTIFIED BY 'replace_with_a_secure_password';
	GRANT ALL PRIVILEGES ON newsdb.* TO 'newsuser'@'localhost';
	FLUSH PRIVILEGES;
	EXIT;
	```

5. Create your local configuration file and update its password values to match the database user you created.

	```powershell
	Copy-Item .env.example .env
	```

	`.env` contains `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`. It is excluded from Git; do not commit credentials.

6. Apply migrations and start the application.

	```powershell
	python manage.py migrate
	python manage.py runserver
	```

	Open `http://127.0.0.1:8000/`.

## Docker Compose Setup

Prerequisite: Docker Desktop must be installed and its engine must be running.

1. Clone the repository and enter the new project folder.

	```powershell
	git clone https://github.com/nathankap/news-app-capstone.git
	cd news-app-capstone
	```

2. Create the Docker environment configuration and replace the example password values.

	```powershell
	Copy-Item .env.example .env
	```

3. Build and start the Django and MariaDB containers.

	```powershell
	docker compose up --build
	```

	Docker Compose creates the MariaDB database from `.env`, waits for it to become available, applies migrations, and serves the app at `http://127.0.0.1:8000/`.

4. Stop the containers when finished.

	```powershell
	docker compose down
	```

	Use `docker compose down -v` only when you also want to remove the persisted database data.

## Documentation and Tests

Generated Sphinx documentation is in `docs/_build/html/index.html`. Rebuild it with:

```powershell
python -m sphinx -b html docs/source docs/_build/html
```

Run the test suite with:

```powershell
python manage.py test news_app
```

### Optional SQLite Setup

MariaDB is the required default. For a temporary SQLite-only experiment, change the `DATABASES['default']` settings to Django's SQLite configuration; do not use that configuration for the standard project setup.
