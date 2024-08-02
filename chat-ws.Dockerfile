FROM python:3.10-slim

# Set pip to have no saved cache
ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

CMD ["python", "-m", "chat_ws"]

WORKDIR /app

RUN pip install -U poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

ARG git_sha="development"
ENV GIT_SHA=$git_sha

COPY . .
