# Version 0.1.0
FROM continuumio/anaconda
MAINTAINER your name "dennis gannon"
RUN pip install azure-storage
RUN easy_install bottle
COPY azure-bottle-table-service.py /
COPY script2.sh /
ENTRYPOINT ["bash", "/script2.sh"]
