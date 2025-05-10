from datetime import datetime


def time_format(dt: datetime) -> str:
    
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")