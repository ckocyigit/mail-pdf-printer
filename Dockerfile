FROM python:3.6-alpine

ADD . /script

RUN pip install -r /script/requirements.txt

CMD python /script/mailprinter.py
