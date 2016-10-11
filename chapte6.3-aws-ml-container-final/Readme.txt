This directory contains two subdirectories.
1. new-predictor.   this is the service that pulls records from the aws queue and does the analysis.  You will need to uncompress the data files.  
2. table-manager.  This is the container for the web service that waits for requests (which are json files and load them into the Azure nosql table.  
It also contains two jupyter notebooks.
1.  load_sciml_data_send_to_aws_queue read and loads the data file (sciml_data_arxiv.p) and pushes it to the aws queue.
2.  boto3ecs is the notebook that can configure each of the two containers as services for AWS ECS

Security:  not that the containers make specific references to your AWS keys.   This is not good.  A better solution is to change the containers so that these keys are passed in as arguments from the service descriptions and serivce creation steps.

