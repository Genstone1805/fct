FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=fct.settings

WORKDIR /app

# System deps (mysqlclient needs these)
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . .

# Collect static ONCE (WhiteNoise requirement)
RUN python manage.py collectstatic --noinput

EXPOSE 1805

CMD ["gunicorn", "--bind", "0.0.0.0:1805", "fct.wsgi:application"]
