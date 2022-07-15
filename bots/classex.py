"""
Classex (auXiliar classes) for Xipato Bot
Author: João Fonseca
Date: 13 July 2022
"""

import time

class SleepData:
    '''
    Data Type for sleeps in bot pooling
    Receives:       [up_time, {time1: [[start1,end1],[start2,end2],...], ...}]
    Transforms to:  [hour0_sleep, ..., hour23_sleep, up_time]

    self.up [is it up time? (0/1), loops in uptime left]
    '''

    def __init__(self, time_dix):
        sleeps = [0]*25
        dix = time_dix[1]
        keys = dix.keys()
        for key in keys:
            deltas = dix[key]
            for delta in deltas:
                for i in range(delta[0],delta[1]):
                    sleeps[i] = key
        sleeps[24] = time_dix[0]
        self.sleeps = sleeps
        self.up = [0,0] 

    def start_uptime(self, minutes):
        if minutes == 0:
            self.up = [0,0]
        else:
            self.up = [1,((minutes*60)//self.sleeps[24])]


    def set_uptime_sleep(self,sleep):
        self.sleeps[24] = sleep

    def get_current_sleep(self):
        if self.up[0]==1:
            self.up[1]-=1
            if self.up[1] == 0:
                self.up = [0,0]
            return self.sleeps[24]
        return self.sleeps[(time.localtime().tm_hour)]

    def set_hour_sleep(self, hour, sleep):
        self.sleeps[hour] = sleep

    def set_interval_sleep(self, delta, sleep):
        for i in range(delta[0],delta[1]):
            self.sleeps[i] = sleep


class XiPatoDefaultSleep(SleepData):

    def __init__(self):
        xipato_time = [   
            5,                                  #Up time                        
            {300:   [[4,7]],                    # Low       5min
            120:    [[2,4],[7,8]],              # Mid Low   2min
            60:     [[8,9],[0,1]],              # Mid       1min
            20:     [[9,13],[17,20],[23,0]],    # Mid High  20sec
            10:     [[13,17],[20,23]]}          # High      10sec
        ]  
        super().__init__(xipato_time)        
        




        
            

