FROM python3.10

WORKDIR /app

ADD . /app

RUN pip install requirements.txt

CMD ["flask",  "run"]
