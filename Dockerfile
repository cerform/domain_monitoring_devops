# -------------------------------
# Base image: lightweight Python 3.12
# -------------------------------
FROM python:3.12-slim

# -------------------------------
# Environment
# -------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# -------------------------------
# Install ONLY light dependencies
# -------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        unzip \
        gnupg \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# -------------------------------
# Project directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Copy files
# -------------------------------
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# -------------------------------
# Expose port
# -------------------------------
EXPOSE 8080

# -------------------------------
# Start application
# -------------------------------
CMD ["python", "app.py"]
