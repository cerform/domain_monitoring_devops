# Use a lightweight official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /domain_monitoring_system

# Copy dependency file
COPY requirements.txt .

# Install dependencies, including pytest and selenium
RUN pip install --no-cache-dir -r requirements.txt pytest selenium

# Install Google Chrome and matching ChromeDriver
RUN apt-get update && apt-get install -y wget gnupg unzip curl ca-certificates \
    && mkdir -p /etc/apt/keyrings \
    && wget -q -O /etc/apt/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    \
    # Get Chrome major version (e.g. 142)
    && CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+' | head -1) \
    \
    # Fetch matching ChromeDriver version automatically
    && DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION}") \
    && wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /var/lib/apt/lists/* /tmp/*


# Copy project files
COPY . .

# Expose default port
EXPOSE 5000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command
CMD ["python", "app.py"]
