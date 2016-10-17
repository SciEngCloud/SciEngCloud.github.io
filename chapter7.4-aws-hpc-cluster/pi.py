import sys
from math import *
import time

myid = sys.argv[1]
myip = sys.argv[2]
#print 'myid = '+str(myid)

sum = 0.0
for i in range(1,100000000):
	sum = sum + 1.0/(i**2)
pi = sqrt(6.0*sum)

fi = open('/home/ec2-user/outfiles/out'+str(myid), 'w')
fi.write( "pi = "+str(pi)+' from '+str(myid) + " on host "+str(myip))
fi.close()
time.sleep(10)