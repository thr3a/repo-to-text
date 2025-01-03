FROM --platform=linux/x86_64 python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=on
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ADD main.py /

ENTRYPOINT ["python3", "/main.py"]
