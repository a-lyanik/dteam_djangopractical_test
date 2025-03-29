# Use the latest Python image
FROM python:3.13

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project dependencies
COPY pyproject.toml poetry.lock /app/

# Copy readme....its 2 am.....poetry needs readme...why are we here, just to suffer?
COPY README.md /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the entire project
COPY . /app/

# Expose port 8000
EXPOSE 8000

RUN ls -la
