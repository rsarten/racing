import re
import calendar

def date_from_link(link):
    date_comp = re.findall(r'(?<=Key=)[A-Za-z0-9]*(?=,)', link)[0]
    year = date_comp[0:4]
    month = str(list(calendar.month_abbr).index(date_comp[4:7]))
    month = month.rjust(2, "0")
    day = date_comp[-2:]
    return year+"-"+month+"-"+day

def clean_venue(venue):
    return re.sub(" [A-Z]+$", "", venue)

def int_or_0(x):
    try:
        x = int(x)
    except:
        x = 0
    return x

def float_or_0(x):
    try:
        x = float(x)
    except:
        x = 0.0
    return x