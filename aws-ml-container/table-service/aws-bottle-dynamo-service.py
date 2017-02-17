import boto3
from socket import gethostname
hostnm = gethostname()
import time
from bottle import route, request, run
import json


## the following is an unsecure way to controll access
## a better solution is to use docker secret repository
## or to pass this information as a command line parameter 
## when the instance is started.
## or even better:  use an aws ami role. 
#access_key = 'your key'
#secret_key = 'your secret key'

# create a dynamo db table for the results
dyndb = boto3.resource('dynamodb',
    region_name='us-west-2',
#    aws_access_key_id=access_key,
#    aws_secret_access_key=secret_key
 )
 
try:
    table = dyndb.create_table(
        TableName='BookTable',
        KeySchema=[
            {
                'AttributeName': 'PartitionKey',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'RowKey',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PartitionKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'RowKey',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
except:
     #if there is an exception, the table may already exist.   if so...
    table = dyndb.Table("BookTable")
print('table created and ready')

@route('/save_to_table', method='POST')
def save_to_table():
	st = request.forms.get('string')
	#print st
	timestamp = time.time()
	dic = json.loads(st)
	metadata_item = {'PartitionKey': dic['hostnm'], 'RowKey': dic['RowKey'], 
	   'date' : str(timestamp), 'answer': dic['answer'], 
	   'predicted': dic['predicted'], 'title': dic['title']}
	#print "metadata_item ="+str(metadata_item)
	try:
		table.put_item(Item=metadata_item)
		#print "got the arg:"+st
	except:
		return "item may already be there or another failure"
	
	return "table loaded from "+hostnm
 
run(host='0.0.0.0', port=8050)

#goes in the next call
metadata_item = {'PartitionKey': hostnm, 'RowKey': str(i), 
                'date' : str(timestamp), 'answer': source, 'predicted': str(predicted), 'title': title}
try:
   table.put_item(Item=metadata_item)
except:
    print("item may already be there or another failure")

