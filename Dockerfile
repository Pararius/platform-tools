# NOTE: this image is never used in production and only serves to provide a consistent environment for all developers and workflows
FROM python:3.9.6-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      python3-dev \
;

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -U \
        black \
        pytest \
        setuptools \
;

COPY . /app

WORKDIR /app

RUN python -m pip install -e .
