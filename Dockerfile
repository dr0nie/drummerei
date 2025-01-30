FROM python:3.12-alpine as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM builder

WORKDIR /app

COPY . .

RUN sh create_env.sh
RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput --username admin --email ""
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
