import boto3
import sys
from socket import gethostname
from predictor import predictor
hostnm = gethostname()
import time
import socket
import requests
import json
from socket import gethostname
hostnm = gethostname()

#We need IP address of of the host that is running our webservice.
#it is stored in /ipaddr by the script that called invoked this program
#using the magic of the container gateway as follows
#netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}' > /ipaddr

f = open('/ipaddr', 'r')
w = f.read()
webservice = w[:-1]

print 'webservice = '+ webservice
print 'port of table service ='+sys.argv[1]
port = sys.argv[1]

pred = predictor()

## the following is an unsecure way to controll access
## a better solution is to use docker secret repository
## or to pass this information as a command line parameter 
## when the instance is started.
# even better: for AWS we will use the IAM role we created
# as described in the text

access_key = 'YOUR AWS ACCCESSS KEY'
secret_key = 'YOUR AWS Secrect key'



sqs = boto3.resource('sqs',
        region_name='us-west-2', 
		aws_access_key_id = access_key,
		aws_secret_access_key = secret_key
		)
queuename = 'bookque'
try:
    queue = sqs.create_queue(QueueName=queuename) # Attributes={'DelaySeconds': '5'})
except:
    print("queue %s exists"%queuename)
    queue = sqs.get_queue_by_name(QueueName=queuename)

print(queue.url)
print(queue.attributes.get('DelaySeconds'))

def sendrest(row, answer, predict, title):
	try:
		addr ="http://"+webservice+":"+port+"/save_to_table"
		dic = { 'RowKey': row, 'answer': answer, 'predicted': predict, 'title': title, 'hostnm':hostnm}
		st = json.dumps(dic)
		payload = {'string':st}
		#print 'sending :'+ str(payload)
		failed = True
		maxtries = 0
		while (failed == True and maxtries < 5):
			try:
				r = requests.post(addr, data=payload)
				failed = False
				#print 'success!'
			except:
				print 'post error'
				maxtries = maxtries +1
				time.sleep(0.2)
				if (maxtries == 5):
					 return False
		#print "got reply:"+r.content
		return True
	except:
		#print "error in sendrest"
		return False


i = 0
while True:
	for message in queue.receive_messages(MessageAttributeNames=['Title', 'Abstract','Source']):
		timestamp = time.time()
		deletemes = True
		if message.message_attributes is not None:
			title = message.message_attributes.get('Title').get('StringValue')
			abstract = message.message_attributes.get('Abstract').get('StringValue')
			source = message.message_attributes.get('Source').get('StringValue')
			predicted = pred.predict(abstract, source)
			deletemes = sendrest(str(i), source, str(predicted), title)
		if deletemes:
			message.delete()
		i = i+1
		#print "delted %s messages"%str(i)
