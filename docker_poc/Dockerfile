FROM python:3.8-slim-buster

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --user -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "dazzle-scrape.py" ]