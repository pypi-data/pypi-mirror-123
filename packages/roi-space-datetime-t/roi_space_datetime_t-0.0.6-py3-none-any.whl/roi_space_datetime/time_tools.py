import time

import datetime


class TimeTool():

    def utc_format(utc_str):
        """将utc时间格式化

        Args:
            utc (datetime): 带tz的utc格式
        Returns:
            [datetime]: utc格式
        """
        utc_str = utc_str.split('.')[0]
        utc_time = datetime.datetime.strptime(utc_str.replace(
            'T', ' ').replace('Z', ''), "%Y-%m-%d %H:%M:%S")
        return utc_time

    def utc_now_time():
        """当前utc时间

        Args:
            utc_time (datetime): utc时间，包含ms

        Returns:
            utc_time: utc格式时间，不包含ms
        """
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        utc_time = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return utc_time

    def hours(seconds):
        """秒转小时

        Args:
            seconds （int): 秒数
        Returns:
            hour: 小时
        
        """
        hour = round(seconds / 3600, 2)
        print("hours: ", hour)
        return hour
    
    def utc_local_time(utc_str):
        """utc时间转本地时间

        Args:
            utc_str (string): 转datetime，并加8得到本地实际 2021-07-30T05:56:00Z
        """
        utc_str = utc_str.split('.')[0]
        
        utc_time = datetime.datetime.strptime(utc_str.replace(
            'T', ' ').replace('Z', ''), "%Y-%m-%d %H:%M:%S")
        
        shanghai_time = utc_time+datetime.timedelta(hours=8)
        return shanghai_time
        

