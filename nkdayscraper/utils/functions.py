import datetime as dt

def getTargetDate():
    today = dt.date.today()
    if today.weekday() in [5, 6]:
        targetDate = today
    else:
        targetDate = today - dt.timedelta((today.weekday() + 1) % 7)

    return targetDate
