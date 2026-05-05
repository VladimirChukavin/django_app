FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==2.4.0"
RUN poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./
COPY training_django_project .

RUN poetry install

CMD ["gunicorn", "training_django_project.wsgi:application", "--bind", "0.0.0.0:8000"]