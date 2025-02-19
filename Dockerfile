# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12 as build
ENV PYTHONWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN mkdir /code
WORKDIR /code

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

FROM build as migrate
COPY entrypoint.sh /code/
RUN ["chmod", "+x", "/code/entrypoint.sh"]
RUN ["chmod", "+x", "/code/bin/wait-for-it.sh"]
ENTRYPOINT ["bash", "/code/entrypoint.sh"]