from toolkit import celery
import time

@celery.task(bind=True, name="toolkit.routes.audit.api.my_background_task")
def my_background_task(self,url):
    print(url)
    for i in range(100):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': 100,
                                'status': "Hello " + str(i)})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

