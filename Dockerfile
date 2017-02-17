# Version 0.1.0
FROM ipython/scipystack
MAINTAINER dbgannon "dbgannon@gmail.com"
RUN easy_install boto3
RUN easy_install pattern
RUN easy_install nltk
RUN easy_install gensim
COPY models /
COPY config /
COPY predictor.py /
COPY aws-queue-new.py /
COPY script2.sh /
ENTRYPOINT ["bash", "/script2.sh"]
