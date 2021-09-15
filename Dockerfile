# NOTE: this image is never used in production (relies on Google's runtime), it only serves to mimick production as much as possible for development purposes.
FROM python:3.9.6-slim-buster

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -U \
        black \
        pytest \
;
