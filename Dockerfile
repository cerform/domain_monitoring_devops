FROM python:3.12-slim
RUN mkdir /domain_monitoring_system
RUN chmod 777 /domain_monitoring_system
COPY . /domain_monitoring_system
WORKDIR /domain_monitoring_system
RUN pip install -r requirements.txt
CMD ["python", "app.py"]