FROM python:3.9

ADD . /script

RUN  apt-get update && \
     apt-get install -y cups cups-client lpr cups-bsd && \
     pip install -r /script/requirements.txt

CMD python /script/mailprinter.py
