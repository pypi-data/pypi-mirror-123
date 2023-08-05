from datetime import datetime


# 时间格式处理
def format_datetime(utc_time):
    local_time = utc_time + datetime.timedelta(hours=8)
    local_time = "%s年%s月%s日 %s:%s" % (
        local_time.year, local_time.month, local_time.day, str(local_time.hour).zfill(2),
        str(local_time.minute).zfill(2))
    return local_time


# 时间格式处理
def format_datetime_func(utc_time):
    local_time = utc_time + datetime.timedelta(hours=8)
    local_time = "%s年%s月%s日" % (
        local_time.year, local_time.month, local_time.day)
    return local_time


# 获取处理后的当前时间
def func_date_time():
    tz = pytz.timezone('Asia/Shanghai')
    date = datetime.datetime.now(tz)
    if date.minute < 10:
        date = "%s年%s月%s日 %s: 0%s" % (date.year, date.month, date.day, date.hour, date.minute)
    else:
        date = "%s年%s月%s日 %s: %s" % (date.year, date.month, date.day, date.hour, date.minute)
    return date
