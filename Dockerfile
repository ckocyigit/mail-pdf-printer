FROM python:3.6-alpine

ADD . /skript

CMD python /skript/mailprinter.py