netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}' > /ipaddr
cp /predictor.py .
cp /aws-queue-new.py .
ipython2 aws-queue-new.py
