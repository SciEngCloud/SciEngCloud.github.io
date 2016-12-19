cp /predictor.py .
cp /celeryPred.py .
export C_FORCE_ROOT='true'
export GOOGLE_APPLICATION_CREDENTIALS='/your-google-keys.json'
echo $C_FORCE_ROOT
celery worker -A celeryPred -b $1
