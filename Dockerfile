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

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN chmod +rwx /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip install selenium==3.8.0

RUN pip install -r requirements.txt

# ENV PORT = 5000

# ENTRYPOINT [ "python" ]

CMD python app.py --host 0.0.0.0 --port $PORT
