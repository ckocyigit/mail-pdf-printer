FROM python:3.6-alpine

ADD . /script

CMD python /script/mailprinter.py