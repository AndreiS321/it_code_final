FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

RUN python manage.py migrate

RUN python manage.py createsuperuser --noinput
CMD ["python", "manage.py", "runserver", "0:8000"]
