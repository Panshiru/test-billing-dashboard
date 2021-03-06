import logging
import sys

import psycopg2


class DBConnection(object):

    def __init__(self, host, port, user, password, dbname,
                 schema, billing_table, auth_table):
        self.logger = logging.getLogger(__name__)

        self.schema = schema
        self.billing_table = billing_table
        self.auth_table = auth_table

        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

        try:
            self._connect()
        except:
            print >> sys.stderr, 'factory connection error.'

    def _connect(self):
        self.conn = psycopg2.connect(
            host=self.host, port=self.port, database=self.dbname, user=self.user, password=self.password)
        self.cursor = self.conn.cursor()
        self.logger.debug('Postgres db {} connected.'.format(self.dbname))

    def _disconnect(self):
        self.conn.close()
        self.logger.debug('Postgres db {} disconnected.')

    def __del__(self):
        self._disconnect()

    # protected method which can be inherited
    def _select(self, column, schema, table, distinct=False, **kwargs):
        '''
        Generate a select cluase
        :param column:
        :param schema:
        :param table:
        :param distinct:
        :param kwargs:
        :return:
        '''
        if distinct:
            SELECT_STATEMENT = """
                SELECT DISTINCT %s FROM %s.%s
                """ % (column, schema, table)
        else:
            SELECT_STATEMENT = """
                SELECT %s FROM %s.%s
                """ % (column, schema, table)
        if len(kwargs) > 0:
            SELECT_STATEMENT += " WHERE "
            for key, value in kwargs.items():
                if key == 'date' and value == 'history':
                    continue
                SELECT_STATEMENT += "%s = '%s' AND " % (key, value)
            SELECT_STATEMENT = SELECT_STATEMENT[:-5]
        return SELECT_STATEMENT
