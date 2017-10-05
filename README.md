# CloudBook ExamplesThis contains the code samples and demos for the book "Cloud Computing for Science and Engineering".   Most of these samples are Jupyter Notebooks.   If you do not have a copy of Jupyter you should download and install anaconda from Continuum Analytics [https://www.continuum.io/downloads](https://www.continuum.io/downloads ).  Another way to run Jupyter is to install Docker and run the jupyter/scipy-notebook container as followsdocker run -d -p 8888:8888 -e PASSWORD="yourword" -e USE_HTTPS=yes jupyter/scipy-notebookthen go to https://localhost:8888 or, if you started this on a remote host use the ip address of the remote host. ## Contents

### arvix_data
This folder contains the files needed to do the simple document classification experiments using the science abstract from ArXiv catalog. these are used in aws-ml-container for examples in chapter 7.6.
The notebook doc_analysisd7-physics.ipynb illustrates how to build the models for analyzing the physics documents.   

### aws-hpc-cluster
This is a folder containing the files need to deploy an HPC cluster on AWS using CfnCluster.  It is described in chapter 7.2.3 "Scale"

### aws-ml-container
is the files needed to build the containers used in the AWS container service demo from chapter 7.6

### datadir
contains the simple files used in the chapter 3, using cloud storage

### Docker-demo
is the source for the docker sample in section 6.4 in the containers chapter

### gcloud-container
celery gcloud kubernetes example again using the arxiv document predictor service.

### kinesis-spark-AoT
this is the simple kinesis to spark example from 9.4 streaming data chapter.

### movie7.gif
this is the output of the movie created by the autoencoder.ipynb example discussed in the autoencocer supplement 

### notebooks
This folder contains all the ipython notebooks

### sc-tutorial
contains the lectures and exercises for the sc17 tutorial

### singularity
is a folder containing some of the files for the singularity supplement


