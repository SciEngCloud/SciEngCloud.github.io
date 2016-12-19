from celery import Celery
from socket import gethostname
from predictor import predictor
from gcloud import datastore
clientds = datastore.Client()
key = clientds.key('booktable')
hostnm = gethostname()
import time

app = Celery('predictor', backend='amqp')

pred = predictor()

	
#define the functions we will call remotely here
@app.task
def predict(abstract, title, source):
	prediction = pred.predict(statement, source)
	entity = datastore.Entity(key=key)
	entity['partition'] = hostname'
	entity['date'] = str(time.time())
	entity['title' ] = title
	entity['prediction'] = str(prediction)
	clientds.put(entity)
	return [prediction]