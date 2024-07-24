FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip
RUN pip install pipenv

COPY . /app
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system

EXPOSE 9999
CMD ["python", "ips.py"]
