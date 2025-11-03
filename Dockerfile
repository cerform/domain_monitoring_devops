FROM python:3.12-slim
RUN mkdir /domain_monitoring_system
RUN chmod 777 /domain_monitoring_system


COPY . /domain_monitoring_system


WORKDIR /domain_monitoring_system


RUN apt-get update && apt-get install -y  --no-install-recommends curl \
    && apt-get clean && rm -rf /var/lib/lists/* /var/cache/apt/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN pip install pytest selenium


CMD ["python", "app.py"]
