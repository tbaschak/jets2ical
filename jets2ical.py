#!/usr/bin/env python

import pandas as pd
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
import pytz
import tempfile, os

def month_to_int(x):
    return {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }[x]

def int_to_month(x):
    return {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec',
    }[x]

def parsedate(pdate, pyear):
    #nothing
    month, day = pdate.split(' ')
    if (month == 'Jan') or (month == 'Feb') or (month == 'Mar') or (month == 'Apr') or (month == 'May'):
        pyear += 1
    #return pyear, month_to_int(month), int(day)
    return pyear, month_to_int(month), int(day)

def parsetime(ptime):
    ltime, ampm = ptime.split(' ')
    lhours, lminutes = ltime.split(':')
    if ampm == 'PM':
        lhours = int(lhours) + 12
    else:
        lhours = int(lhours)
    lminutes = int(lminutes)
    return lhours, lminutes

year = 2017
url = 'https://www.nhl.com/jets/schedule/2017/CT/print'
stuff = pd.read_html(url, header=0)
col1 = stuff[0]
col2 = stuff[1]

cal = Calendar()
cal.add('prodid', '-//Jets Home Games//bgp.guru//')
cal.add('version', '2.0')

for row in col1.itertuples():
    if "@" not in row[4]:
        lyear, lmonth, lday = parsedate(row[2], year)
        lhour, lminutes = parsetime(row[3])
        #print "%s %d, %d @ %s - %s" % (int_to_month(lmonth), lday, lyear, row[3], row[4])
        event = Event()
        event.add('summary', 'Jets ' + row[4])
        event.add('dtstart', datetime(lyear, lmonth, lday, lhour, lminutes, 0, tzinfo=pytz.timezone('US/Central')))
        event.add('dtend', datetime(lyear, lmonth, lday, lhour + 3, lminutes, 0, tzinfo=pytz.timezone('US/Central')))
        event['location'] = vText('300 Portage Ave, Winnipeg, MB R3P5S4')
        cal.add_component(event)

for row in col2.itertuples():
    if "@" not in row[4]:
        lyear, lmonth, lday = parsedate(row[2], year)
        lhour, lminutes = parsetime(row[3])
        #print "%s %d, %d @ %s - %s" % (int_to_month(lmonth), lday, lyear, row[3], row[4])
        event = Event()
        event.add('summary', 'Jets ' + row[4])
        event.add('dtstart', datetime(lyear, lmonth, lday, lhour, lminutes, 0, tzinfo=pytz.timezone('US/Central')))
        event.add('dtend', datetime(lyear, lmonth, lday, lhour + 3, lminutes, 0, tzinfo=pytz.timezone('US/Central')))
        event['location'] = vText('300 Portage Ave, Winnipeg, MB R3P5S4')
        cal.add_component(event)

dir_path = os.getcwd()
f = open(os.path.join(dir_path, 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()
