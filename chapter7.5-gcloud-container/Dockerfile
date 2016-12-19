# Version 0.1.0
FROM ipython/scipystack
MAINTAINER dbgannon "dbgannon@gmail.com"
RUN easy_install celery
RUN pip install -U Sphinx
RUN pip install gcloud
RUN easy_install pattern
RUN easy_install nltk
RUN easy_install gensim
COPY bookproject-key.json /
COPY models /
COPY config /
COPY sciml_data_arxiv.p /
COPY predictor.py /
COPY celeryPred.py /
COPY script.sh /
ENTRYPOINT ["bash", "/script2.sh"]
