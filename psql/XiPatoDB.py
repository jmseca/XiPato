'''
Defining Functions to manage XiPato DB
Author: João Fonseca
Date: 31 July 2022
'''

import psycopg2
import psycopg2.extras
import os
from time import sleep

from exceptions import *

class XiPatoUser:

    basedir = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, host, user, pword, max_retries=10):
        self.connection_string = f'host={host} dbname={user} user={user} password={pword}'
        self.max_retries=max_retries
        try:
            dbConn = psycopg2.connect(self.connection_string)
            dbConn.close()
            print('Connection is possible')
        except:
            raise DBFailedConnectionException()

    def get_query_from_file(self, filename):
        query_file_pre = os.path.join(self.basedir, f"queries/{filename}")
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
        return query

    def commit_close(self, conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    def get_ads_urls(self):
        tried,done = 0,False
        while (tried<self.max_retries) and not(done):
            try:
                dbConn = psycopg2.connect(self.connection_string)
                cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                cursor.execute(self.get_query_from_file('ads_urls.txt'))
                done = True
            except:
                tried+=1
                sleep(2)
            finally:
                self.commit_close(dbConn,cursor)   
        if tried==10:
            raise DBMaxRetriesExceededException('getting ads\' urls')
        else:
            return [url for url in cursor.fetchall()]

    def update_sold_ad(self, cursor, ad):
        #data = (ad.car_id, ad.)
        #cursor.execute()
        pass
        

    def update_sold(self, *new_sold ):
        '''
        Updates DB when ads ae sold
        '''
        if new_sold!=():
            tried,done = 0,False
            while (tried<self.max_retries) and not(done):
                try:
                    dbConn = psycopg2.connect(self.connection_string)
                    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                    cursor.execute('start transaction;')
                    for ad in new_sold:
                        self.update_sold_ad(cursor,ad)
                    done = True
                except:
                    tried+=1
                    sleep(2)
                finally:
                    self.commit_close(dbConn,cursor)   
            if tried==10:
                raise DBMaxRetriesExceededException('updating sold ads')

