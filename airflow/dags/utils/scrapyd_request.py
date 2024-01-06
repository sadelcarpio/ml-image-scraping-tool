def check_status(ti):
    import time
    import requests
    import json
    import logging

    logger = logging.getLogger(__name__)
    response_status = ti.xcom_pull(task_ids='schedule-spider')
    response_status = json.loads(response_status)
    job_id = response_status["jobid"]
    try:
        job_finished_status = []
        while not job_finished_status:
            response = requests.get('http://scrapyd:6800/listjobs.json', timeout=10)
            response.raise_for_status()
            finished = response.json()['finished']
            running = response.json()['running']
            job_finished_status = list(filter(lambda job: job["id"] == job_id, finished))
            if job_finished_status:
                logger.info(f"Web scraping finished: {job_finished_status[0]}")
                return
            job_running_status = list(filter(lambda job: job["id"] == job_id, running))
            logger.info(f"Web scraping status: {job_running_status[0]}")
            time.sleep(30)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error on HTTP request: {e}")
        return
