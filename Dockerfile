FROM python:3.11-alpine3.16
LABEL maintainer="Shivam Patel <shivam.patel.nhsf@gmail.com>"
RUN apk add --update --no-cache curl build-base postgresql-dev
RUN apk add --no-cache bzip2-dev \
        coreutils \
        gcc \
        libc-dev \
        libffi-dev \
        libressl-dev \
        linux-headers \
        jpeg-dev \
        zlib-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        libxml2-dev \
        libxslt-dev \
        postgresql-client
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=. \
    PIP_NO_CACHE_DIR=yes \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH=/root/.local/bin:$PATH \
    POETRY_VERSION=1.4.2 \
    PYTHONPATH=.
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false --local
RUN poetry run python -m pip install -U pip
RUN poetry install
RUN poetry run python -m pip install pydantic[email]
RUN poetry install
RUN adduser -D app  # Changed to create a system user
USER root
COPY --chown=app:wheel . /app/
EXPOSE 8080
HEALTHCHECK CMD curl --fail http://localhost:8080/health || exit 1
CMD ["./scripts/run.sh"]
