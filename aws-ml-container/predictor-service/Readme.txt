First uncompress models.tar.gz

tar -xf models.tar.gz

then build the predictor

docker build -t yourname/predictor .

then  push to the docker hub 

docker push yourname/predictor


