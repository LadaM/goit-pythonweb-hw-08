# Use the official Python 3.11 image as a base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the pyproject.toml and poetry.lock files to install dependencies
COPY pyproject.toml poetry.lock /usr/src/app/

# Install Poetry and project dependencies
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the entire application directory into the container
COPY . /usr/src/app/

# Ensure the `.env` file is accessible
COPY .env /usr/src/app/.env

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the application using uvicorn
CMD ["uvicorn", "app.utils.main:app", "--host", "0.0.0.0", "--port", "8000"]
