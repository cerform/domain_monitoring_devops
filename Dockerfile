FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# -------------------------------
# Install dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates \
    xvfb libxi6 libxss1 libasound2 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libnss3 libgdk-pixbuf-xlib-2.0-0 \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Use chromium instead of google-chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# -------------------------------
# Python dependencies
# -------------------------------
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
