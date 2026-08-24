Quick Start
===========

Run with Python (venv)
----------------------

1. Create and activate a virtual environment.

   .. code-block:: powershell

      python -m venv .venv
      .\\.venv\\Scripts\\Activate.ps1

2. Install dependencies.

   .. code-block:: powershell

      pip install -r requirements.txt

3. Apply database migrations.

   .. code-block:: powershell

      python manage.py migrate

4. Start the app.

   .. code-block:: powershell

      python manage.py runserver 0.0.0.0:8000

5. Open in browser.

   ``http://127.0.0.1:8000``

Run with Docker
---------------

1. Build the Docker image.

   .. code-block:: powershell

      docker build -t news-app:latest .

2. Run the container.

   .. code-block:: powershell

      docker run --rm -p 8000:8000 news-app:latest

3. Open in browser.

   ``http://127.0.0.1:8000``
