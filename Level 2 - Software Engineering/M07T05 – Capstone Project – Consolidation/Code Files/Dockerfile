# Use a small supported Python image as the base image.
FROM python:3.12-slim

# Prevent bytecode files and send Python output directly to the container log.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Store the application inside the container's working directory.
WORKDIR /app

# Install the compiler and MariaDB client libraries required by mysqlclient.
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	default-libmysqlclient-dev \
	pkg-config \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies before copying source files to reuse Docker cache.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the image.
COPY . /app/

# Document the port used by the Django development server.
EXPOSE 8000

# Run migrations then start Django on all container network interfaces.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
