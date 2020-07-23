redis-server &
python3 run.py &
celery worker -A celery_worker.celery --loglevel=info --pool=solo


