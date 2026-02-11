FROM python:3.12-alpine

WORKDIR /app

# Install build dependencies (often needed for python packages on Alpine)
# RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot_listener.py .

# Environment variables should be passed via docker-compose or run command
CMD ["python", "bot_listener.py"]
