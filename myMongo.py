from pymongo import MongoClient
import logging
import logging.config

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('crawlerLogger')

class CMongoDB(object):
    """docstring for CMongoDB."""
    def __init__(self):
        super(CMongoDB, self).__init__()
        client = MongoClient()
        self.db = client.institutedata

    def insert(self,collection,data,one=True):
        logger.info('INSERTING :: {}'.format(collection))
        if(one):
            self.db[collection].insert_one(data)
        else:
            pass

    def get(self,collection,**kwargs):
        return self.db[collection].find(**kwargs)
