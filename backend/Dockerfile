FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y poppler-utils

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "taxchatter/manage.py", "runserver", "0.0.0.0:8000"]
