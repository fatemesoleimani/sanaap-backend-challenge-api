# Base image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl \
  && curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root


# Copy the rest of the project
COPY . /app/

# Expose Django port
EXPOSE 8000

# Add entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Start the app
CMD ["/app/docker-entrypoint.sh"]
