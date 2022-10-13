# NOTE: this image is never used in production and only serves to provide a consistent environment for all developers and workflows
FROM python:3.10.4-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      python3-dev \
      default-libmysqlclient-dev \
;

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -U \
        black \
        pytest \
        setuptools \
;

WORKDIR /app

COPY setup.py /app/setup.py
COPY README.md /app/README.md

RUN python -m pip install -e .
