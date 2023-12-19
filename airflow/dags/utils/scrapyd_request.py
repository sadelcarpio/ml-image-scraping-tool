import logging

logger = logging.getLogger(__name__)


def check_status():
    import time
    import requests
    try:
        finished = []
        while not finished:
            response = requests.get('http://scrapyd:6800/listjobs.json', timeout=10)
            response.raise_for_status()
            finished = response.json()['finished']
            running = response.json()['running']
            logger.info(f"Web scraping status: {running}")
            time.sleep(30)
        logger.info(f"Web scraping finished: {finished}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error on HTTP request: {e}")
        return
