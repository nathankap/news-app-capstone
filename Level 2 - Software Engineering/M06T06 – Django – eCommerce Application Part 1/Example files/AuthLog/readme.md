---

# AuthLog Django Project

This is a Django eCommerce web application with two main apps:

* **grabsomore**: Handles login, registration, password reset, and user sessions.
* **eCommerce**: Supports vendors, stores, products, carts, checkout, order emails, reviews, and permissions.

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Password Reset Testing](#password-reset-testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Python 3.9 or later installed. [Download Python](https://www.python.org/downloads/)
* MySQL installed and running on your machine.
* Basic knowledge of using the command line / terminal.
* Git installed to clone the repository (optional but recommended).

---

## Installation

1. **Clone the repository** (or download the ZIP and extract):

   ```bash
   git clone https://github.com/yourusername/AuthLog.git
   cd AuthLog
   ```

2. **Create and activate a virtual environment** (recommended):

   * On Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Email Settings:**

   For sending emails (like password resets), update your email credentials in `AuthLog/settings.py` under the email section:

   ```python
   EMAIL_HOST_USER = 'your-email@example.com'
   EMAIL_HOST_PASSWORD = 'your-email-password-or-app-password'
   ```

   > **Note:** For Gmail, you might need to create an App Password and enable "Less secure app access".

---

## Database Setup

1. **Create the MariaDB/MySQL database and user (example):**

   Run the following in your MariaDB/MySQL client (adjust names/passwords):

   ```sql
   CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'strongpassword';
   GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecomuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Configure database connection using environment variables:**

   The project reads DB config from environment variables. Set these in your shell or service manager:

   - `DB_ENGINE=mysql` (optional)
   - `DB_NAME` (e.g. `ecommerce_db`)
   - `DB_USER` (e.g. `ecomuser`)
   - `DB_PASSWORD` (e.g. `strongpassword`)
   - `DB_HOST` (e.g. `localhost`)
   - `DB_PORT` (optional)

   Example (Windows cmd):

   ```cmd
   set DB_ENGINE=mysql
   set DB_NAME=ecommerce_db
   set DB_USER=ecomuser
   set DB_PASSWORD=strongpassword
   ```

3. **Install MySQL/MariaDB Python adapter** if not already installed:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Project

1. **Apply migrations:**

   Run the following commands to create the necessary database tables:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create a superuser** (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to create a user with admin privileges.

3. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

4. **Access the application:**

   * Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * Use the login page at `/`, register users, browse the catalog at `/ecommerce/`, manage stores at `/ecommerce/stores/`, and test password reset functionality.

---

## Usage

* **Authentication (`grabsomore` app):**

  * Login at `/` (root URL)
  * Register at `/register/`
  * Request password reset at `/request-password-reset/`
  * Reset password via emailed token link

* **eCommerce (`eCommerce` app):**

  * View the product catalog at `/ecommerce/`
  * View product details, add to cart, checkout, and leave reviews
  * Vendors and superusers can manage stores and products from `/ecommerce/stores/` and product creation pages

---

## Password Reset Testing

If you want to test password reset functionality without sending real emails:

1. Change email backend in `AuthLog/settings.py` to console:

   ```python
   EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
   ```

2. When you submit a password reset request, the reset link will print in your console/terminal.

3. Copy and paste the link into your browser to reset the password.

---

## Troubleshooting

* **MySQL Client Missing Error:**

  If you get `ModuleNotFoundError: No module named 'mysqlclient'`, install it with:

  ```bash
  pip install mysqlclient
  ```

* **SMTP Authentication Error:**

  Make sure you use correct email and password. For Gmail, you might need to use App Passwords instead of your regular password.

* **Static files not loading:**

  During development, Django serves static files automatically. For production, you need to configure static files properly.

---

## Project Structure

```
AuthLog/
├── AuthLog/
│   ├── settings.py          # Project settings (DB, email, apps)
│   ├── urls.py              # Root URL routing
│   └── wsgi.py
├── grabsomore/              # Authentication app
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── urls.py
│   └── ...
├── eCommerce/               # eCommerce app
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── urls.py
├── manage.py                # Django CLI utility
└── requirements.txt         # Python dependencies
```

---