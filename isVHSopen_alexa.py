#! /usr/bin/python
# coding = utf-8

import requests
from datetime import datetime as dt
from datetime import date, timedelta

def isit():
    r = requests.get("https://api.vanhack.ca/s/vhs/data/door.json")
    d = r.json()

    out = "VHS has been %s" % d['value']
    if d['value'] == "open":
        out = "Yes, " + out
    elif d['value'] == "closed":
        out = "No, " + out

    d['last_updated'] = dt.fromtimestamp(d['last_updated'])
# DEBUG
#    d['last_updated'] = d['last_updated'].replace(month=4, day=5, hour=16)
    
    days_since = (dt.today() - d['last_updated']).days
    
    if (days_since < -1) or (days_since == -1 and d['last_updated'].hour > dt.now().hour):
        since = "Barry messed with the timeline"
        
    elif d['last_updated'].day == dt.today().day:
        if (d['last_updated'].hour%12) == 0:
            since = "noon"
        else:
            since = "{hour} o'clock this {part}".format(
                                                    hour=str(d['last_updated'].hour%12),
                                                    part = "evening" if d['last_updated'].hour > 12 else "morning")
    elif days_since == 0:
        since = "yesterday"
    elif days_since in range (3,6):
        since = str(days_since) + " days ago"
    elif days_since in range(6,13):
        since = "last week"
    else:
        since = " for quite a while"
        
    if since[1:2] == "f":
        out = out + since
    else:
        out = out + " since " + since
    
    return out

if __name__ == "__main__":
    print (isit())
