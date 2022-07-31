'''
Defining Functions to manage XiPato DB
Author: João Fonseca
Date: 31 July 2022
'''

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras
import os
from time import sleep

from exceptions import *

class XiPatoUser:

    def __init__(self, host, user, pword):
        self.connection_string = f'host={host} dbname={user} user={user} password={pword}'
        try:
            dbConn = psycopg2.connect(self.connection_string)
            dbConn.close()
            print('Connection is possible')
        except:
            raise DBFailedConnectionException()

    def commit_close(self, conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    def update_sold_ad(self, conn, cursor, ad):
        pass    

    def update_sold(self, *new_sold, max_retries=10):
        '''
        Updates DB when ads ae sold
        '''
        if new_sold!=():
            tried,done = 0,False
            while (tried<10) and not(done):
                try:
                    dbConn = psycopg2.connect(self.connection_string)
                    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                    for ad in new_sold:
                        self.update_sold_ad(dbConn,cursor,ad)
                    done = True
                except:
                    tried+=1
                    sleep(2)
                finally:
                    self.commit_close(dbConn,cursor)   
            if tried==10:
                raise DBMaxRetriesExceededException('updating sold ads')

