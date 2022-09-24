from datetime import datetime

def get_timestamp() -> str:
    # return yyyy-mm-dd hh-MM-ss
    now = str(datetime.now())
    return now.replace(':', '-')[:now.find('.')]