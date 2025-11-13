# -------------------------------
# Base image: lightweight Python 3.12
# -------------------------------
FROM python:3.12-slim

# -------------------------------
# Environment variables
# -------------------------------
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# -------------------------------
# Install dependencies
# -------------------------------
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/* && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        curl wget unzip gnupg ca-certificates && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/*


# Selenium ENV
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# -------------------------------
# Working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Install Python dependencies
# -------------------------------
COPY requirements.txt .
RUN pip install -r requirements.txt

# -------------------------------
# COPY FULL PROJECT INCLUDING TESTS
# -------------------------------
COPY . /app

# -------------------------------
# Expose port and run
# -------------------------------
EXPOSE 8080
CMD ["python", "app.py"]
