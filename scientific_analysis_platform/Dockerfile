# Dockerfile for the Scientific Analysis Platform Flask Application

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# This includes app.py, and all module directories like data_management, visualization, etc.
# Also copy the 'data' directory which holds the EKG JSON file.
COPY . .

# Make port 5000 available to the world outside this container
# This is the port Flask development server runs on by default (as in app.py)
EXPOSE 5000

# Define environment variables (can be overridden in docker-compose.yml)
# Example: Default Flask settings
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# POSTGRES_DB_URL will be set via docker-compose.yml for linking with the db service.
# For local running without docker-compose, this would need to be set if not using defaults.
# ENV POSTGRES_DB_URL="postgresql://platform_user:platform_secret_password@db_postgis:5432/scientific_platform_dev"
# (Note: 'db_postgis' is the service name from docker-compose, not 'localhost')

# Command to run the application using Gunicorn (recommended for production)
# For development, you might use `flask run`
# Ensure Gunicorn is in requirements.txt if you use it here.
# For now, let's stick to `python app.py` as Gunicorn isn't added yet.
# If Gunicorn was added:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
# Or using the app factory:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
# (Gunicorn might need adjustment for app factory if not standard `app = create_app()`)
# The current app.py has `app = create_app()` at global scope after the factory, so `app:app` should work with Gunicorn.

# For this prototype, running with `python app.py` is sufficient for demonstration.
# The `if __name__ == '__main__':` block in app.py handles app.run().
CMD ["python", "app.py"]
