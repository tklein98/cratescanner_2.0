FROM python:3.8.6-buster

COPY .chromedriver /.chromedriver
COPY crate_scanner /crate_scanner
COPY static /static
COPY templates /templates
COPY static /static
COPY app.py /app.py
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py
COPY .env /.env
COPY Procfile /Procfile


RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
