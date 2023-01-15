FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 --default-timeout=200  install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
