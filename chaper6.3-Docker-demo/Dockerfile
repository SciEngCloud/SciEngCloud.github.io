FROM jupyter/scipy-notebook

MAINTAINER your name <your email>
RUN pip install boto3
RUN pip install bottle
COPY images /images
COPY bottleserver.py /
ENTRYPOINT ["ipython", "/bottleserver.py" ]
