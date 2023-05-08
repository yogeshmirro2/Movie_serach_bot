import time
from datetime import datetime , timedelta
async def get_validation_min(user_date_string):
    current = datetime.now()
    datetime_user_date = datetime.strptime(user_date_string, "%Y-%m-%d %H:%M:%S.%f")
    d1= time.mktime(current.timetuple())
    d2= time.mktime(datetime_user_date.timetuple())
    total_validation_min = int((d2-d1)/60)
    return total_validation_min

async def get_verify_date_return_string(num):
    verify_date = datetime.now()-timedelta(int(num)-1)
    return str(verify_date)

async def get_current_datetime_string():
    return str(datetime.now())
async def get_updated_date(num):
    updated_date = datetime.now()+timedelta(int(num))
    return str(updated_date)
    
