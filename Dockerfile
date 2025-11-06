# Selecting Python lib
FROM python:3.12-slim

# Add work dir
WORKDIR /domain_monitoring_system

# Copy for requirements
COPY requirements.txt .

# Installing Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# УInstalling Chrome & ChromeDriver for Selenium
RUN apt-get update && apt-get install -y wget gnupg unzip curl \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && LATEST_CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${LATEST_CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /var/lib/apt/lists/* /tmp/*

# Copy the project folder
COPY . .

# Open Port
EXPOSE 5000

#
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# run app
CMD ["python", "app.py"]
