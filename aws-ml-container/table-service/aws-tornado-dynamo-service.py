#this is a multithreaded tornado version that can handle at least 4 connections in the
#busy loop below.   most failures occur in connecting to rabbit.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time
import sys
import socket
import boto3
from socket import gethostname
hostnm = gethostname()
import time
import json

from tornado.options import define, options

## the following is an unsecure way to controll access
## a better solution is to use docker secret repository
## or to pass this information as a command line parameter 
## when the instance is started.

access_key = 'your key'
secret_key = 'your secret key'

# create a dynamo db table for the results
dyndb = boto3.resource('dynamodb',
    region_name='us-west-2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
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


define("port", default=8050, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class TableSave(tornado.web.RequestHandler):
		tbl = table
		def post(self):
			global i
			st = self.get_argument("string")
			timestamp = time.time()
			dic = json.loads(st)
			metadata_item = {'PartitionKey': hostnm, 'RowKey': dic['RowKey'], 
			   'date' : str(timestamp), 'answer': dic['answer'], 'predicted': dic['predicted'], 'title': dic['title']}
			try:
				table.put_item(Item=metadata_item)
				self.write("got the arg:"+st)
			except:
				self.write("item may already be there or another failure")

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/save_to_table", TableSave),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(8050)
    http_server.start(0)
    #http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

