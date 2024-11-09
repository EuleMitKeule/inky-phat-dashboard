FROM python:3.12-bookworm as builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --without test --no-root && rm -rf ${POETRY_CACHE_DIR}

FROM python:3.12-slim-bookworm as runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY inky_phat_dashboard inky_phat_dashboard

RUN mkdir /config

ENV CONFIG_FILE_PATH=/config/config.yml
ENV LOG_FILE_PATH=/config/inky_phat_dashboard.log

VOLUME /config
CMD ["python", "-m", "inky_phat_dashboard.__main__"]
