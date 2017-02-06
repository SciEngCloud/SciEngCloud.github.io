# Version 0.1.0
FROM ipython/scipystack
MAINTAINER dbgannon "dbgannon@gmail.com"
RUN easy_install boto3
RUN easy_install bottle
#COPY aws-tornado-dynamo-service.py /
COPY aws-bottle-dynamo-service.py /
COPY script2.sh /
ENTRYPOINT ["bash", "/script2.sh"]
