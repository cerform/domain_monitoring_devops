FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# -------------------------------------------------------
# Install dependencies
# -------------------------------------------------------
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl \
    libnss3 libxss1 libasound2 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------
# Install Google Chrome
# -------------------------------------------------------
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# -------------------------------------------------------
# Install ChromeDriver matching Chrome version
# -------------------------------------------------------
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1); \
    DRIVER_VERSION=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION}); \
    wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip"; \
    unzip chromedriver-linux64.zip; \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver; \
    chmod +x /usr/bin/chromedriver; \
    rm -rf chromedriver-linux64 chromedriver-linux64.zip

ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# -------------------------------------------------------
# App
# -------------------------------------------------------
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
