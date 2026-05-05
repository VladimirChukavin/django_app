FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY training_django_project .

CMD ["gunicorn", "training_django_project.wsgi:application", "--bind", "0.0.0.0:8000"]