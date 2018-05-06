from __future__ import print_function

import json
#import requests
from botocore.vendored import requests
from datetime import datetime as dt
from datetime import date, timedelta

print('Loading function')


def lambda_handler(event, context):
    
    response = {}
    outputSpeech = {}
    reprompt = {}
    out_json = {}
    
    r = requests.get("https://api.vanhack.ca/s/vhs/data/door.json")
    d = r.json()
    
    out = "VHS has been %s" % d['value']
    if d['value'] == "open":
        out = "Yes, " + out
    elif d['value'] == "closed":
        out = "No, " + out
    
    d['last_updated'] = dt.fromtimestamp(d['last_updated'])
    
    # DEBUG
    #    d['last_updated'] = d['last_updated'].replace(day=5, hour=16)
    
    days_since = (dt.today() - d['last_updated']).days
    print (days_since)
    
    if (days_since < -1) or (days_since == -1 and d['last_updated'].hour > dt.now().hour):
        since = "Barry messed with the timeline"
        
    elif d['last_updated'].day == dt.today().day:
        if (d['last_updated'].hour%12) == 0:
            since = "noon"
        else:
            since = "{hour} o'clock this {part}".format(
                                                    hour=str(d['last_updated'].hour%12),
                                                    part = "evening" if d['last_updated'].hour > 12 else "morning")
    elif days_since in [0,1]:
        since = "yesterday"
    elif days_since in range (2,6):
        since = str(days_since) + " days ago"
    elif days_since in range(6,13):
        since = "last week"
    else:
        since = " for quite a while"
        
    if since[1:2] == "f":
        out = out + since
    else:
        out = out + " since " + since
    
    outputSpeech['type'] = "PlainText"
    outputSpeech['text'] = out
    
    response['outputSpeech'] = outputSpeech
    response['shouldEndSession'] = "False"
    
    out_json['version'] = "1.0"
    out_json['response'] = response
    out_json['sessionAttributes'] = {}
    
    return out_json
