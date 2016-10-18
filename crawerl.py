import requests
from bs4 import BeautifulSoup
import logging
import logging.config

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('crawlerLogger')

def init(url):
    logger.info('PARSING :: {}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup
