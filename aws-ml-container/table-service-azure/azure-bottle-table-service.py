import csv
import sys
#import azure.storage
from azure.storage.table import TableService, Entity
from socket import gethostname
hostnm = gethostname()
import time
from bottle import route, request, run
import json


table = TableService(account_name='name of your table', 
                             account_key='the account key 2 for your talbe')
if table.create_table('BookTable'):
    print "table created"
else:
    print "table already there"
	
		
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
		table.insert_entity('BookTable', metadata_item)
		#print "got the arg:"+st
	except:
		return "item may already be there or another failure"
	
	return "table loaded from "+hostnm
 
run(host='0.0.0.0', port=8055)

#goes in the next call
metadata_item = {'PartitionKey': hostnm, 'RowKey': str(i), 
                'date' : str(timestamp), 'answer': source, 
				'predicted': str(predicted), 'title': title}
try:
   table.insert_entity('BookTable', metadata_item)
except:
    print("item may already be there or another failure")

