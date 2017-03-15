First uncompress models.tar.gz

tar -xf models.tar.gz

then build the predictor

docker build -t yourname/predictor .

then  push to the docker hub 

docker push yourname/predictor-new

this version takes an argument which is the port number of
the table service.   you can invoke with
docker run -it dbgannon/predictor-new 8050  for the dynamodb version
docker run -it dbgannon/predictor-new 8055  for the azure table version


