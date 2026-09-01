Quick Start
===========

Run with Python (venv)
----------------------

1. Clone the project and enter its folder.

   .. code-block:: powershell

      git clone https://github.com/nathankap/news-app-capstone.git
      cd news-app-capstone

2. Create and activate a virtual environment inside the project folder.

   .. code-block:: powershell

      python -m venv .venv
      .\\.venv\\Scripts\\Activate.ps1

3. Install dependencies.

   .. code-block:: powershell

      pip install -r requirements.txt

4. Create the MariaDB database and user before continuing.

   .. code-block:: powershell

      mysql -u root -p

   .. code-block:: sql

      CREATE DATABASE newsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
      CREATE USER 'newsuser'@'localhost' IDENTIFIED BY 'replace_with_a_secure_password';
      GRANT ALL PRIVILEGES ON newsdb.* TO 'newsuser'@'localhost';
      FLUSH PRIVILEGES;
      EXIT;

5. Create ``.env`` from ``.env.example`` and update the database password.

   .. code-block:: powershell

      Copy-Item .env.example .env

6. Apply database migrations.

   .. code-block:: powershell

      python manage.py migrate

7. Start the app.

   .. code-block:: powershell

      python manage.py runserver 0.0.0.0:8000

8. Open in browser.

   ``http://127.0.0.1:8000``

Run with Docker
---------------

Docker Desktop must be installed and its engine must be running.

1. Clone the project and enter its folder.

   .. code-block:: powershell

      git clone https://github.com/nathankap/news-app-capstone.git
      cd news-app-capstone

2. Create ``.env`` from ``.env.example`` and replace the example passwords.

   .. code-block:: powershell

      Copy-Item .env.example .env

3. Build and start the Django and MariaDB containers.

   .. code-block:: powershell

      docker compose up --build

   Docker Compose creates the database, waits for MariaDB, and applies
   migrations automatically.

4. Open in browser.

   ``http://127.0.0.1:8000``

5. Stop the containers.

   .. code-block:: powershell

      docker compose down

Optional SQLite Setup
---------------------

MariaDB is the required default. For a temporary SQLite-only experiment,
replace ``DATABASES`` in ``news_project/settings.py`` with:

.. code-block:: python

   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
      }
   }

Do not use this configuration for the standard project setup.
