FROM python:3.11 AS builder

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY app /app

ENTRYPOINT ["python3"]
CMD ["app.py"]
