This directory contains two subdirectories.
1. predictor-service.   this is the service that pulls records from the aws queue and does the analysis.  You will need to uncompress the models files and build the service and save it to the dockerhub  
2. table-service.  This is the container for the web service that waits for requests (which are json files) and load them into the Azure nosql table.  

This directory also contains two jupyter notebooks.
1.  boto3ecs is the notebook that can configure each of the two containers as services for AWS ECS.   You first must create 
2.  load_sciml_data_send_to_aws_queue read and loads the data file (sciml_data_arxiv.p) and pushes it to the aws queue.

You shoud start by going to the portal and creating a ECS service as described in the book.
Security:  For the services to be able to access the aws queue and dynamodb table you need to create a special IAM role as describe in the book.   
