# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* ./

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application's code
COPY . .

# Run the command to start the bot
CMD ["poetry", "run", "python", "main.py"] 