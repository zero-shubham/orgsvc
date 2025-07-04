# Use Python 3.13 as the base image
FROM python:3.13.5-alpine3.22

WORKDIR /orgsvc

RUN apk update && apk add --no-cache \
    build-base \
    python3-dev \
    postgresql-dev \
    && rm -rf /var/cache/apk/* # Clean up apk cache to reduce image size

COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY ./ ./


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]