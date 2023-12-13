# NOTE: this image is never used in production (relies on Google's runtime), it only serves to mimick production as much as possible for development purposes.
FROM python:3.10.4-slim-buster

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        libssl-dev \
        make \
        default-libmysqlclient-dev \
;

COPY requirements.txt ./

ENV PYTHONPATH "$PYTHONPATH:$PWD"

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install -U \
        pytest \
        pytest-mock \
;
