# -*- coding: utf-8 -*-
import sys, pymongo, logging


class MongoDBBase(object):
    def __init__(self, config):
        try:
            host = config['host']
            port = config['port']
            username = config['username']
            password = config['password']
            self._conn = pymongo.MongoClient(host, port)
            self._db = self._conn[config['dbname']]
            self._username = username
            self._password = password

        except Exception as e:
            logging.error("######Connect statics fail")
            sys.exit(1)
        logging.warning("######DB: {0} connect successfully!".format(config['dbname']))

    def close(self):
        self._conn.close()

    def get_coll(self, collname):
        coll = self._db[collname]
        if coll:
            return coll
        else:
            logging.error('Coll: %s not established' % collname)
            return None
