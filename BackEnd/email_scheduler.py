'''
code: email scheduling functionality
group: Wholesome as Heck Programmers
author(s): Thomas Joyce
last modified: 23 Nov 2021
ref:
    https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
    look here for scheduling daily sending functionality. 
--------------------------------------------------------------------------------
                                 IMPORTANT!!!
--------------------------------------------------------------------------------
This must be run with nohup on the machine which will serve as backend. if the 
machine is reset, this will need to be run again. 

to start enter into terminal: nohup py email_scheduler.py &
'''

import time
import schedule
from email_manager import *

def get_users():
    '''
    get every user id and then send each user a workout email using email_mgr
    '''
    users = db_mgr.get_all_rows("users", ["user_id"])
    for user in users:
        get_user(user[0])
        # print(str(user[0]))


schedule.every().day.at("8:30").do(get_users) #send the daily email at 830

while True:
    schedule.run_pending() # do shedule items
    time.sleep(60) # wait one minute then set schedule again after running.