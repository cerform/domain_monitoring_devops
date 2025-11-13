# -------------------------------
# Base: Python 3.12 slim
# -------------------------------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# -------------------------------
# Install system dependencies
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg ca-certificates \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Set environment vars for Selenium
# -------------------------------
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# -------------------------------
# Install Python requirements
# -------------------------------
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Copy project
# -------------------------------
COPY . .

CMD ["pytest", "tests/selenium_tests", "--maxfail=1", "--disable-warnings", "-q"]
