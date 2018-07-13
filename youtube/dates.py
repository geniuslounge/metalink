import dateutil.parser

def day_of_week(int):
    if int == 0:
        return "Mon"
    elif int == 1:
        return "Tue"
    elif int == 2:
        return "Wed"
    elif int == 3:
        return "Thu"
    elif int == 4:
        return "Fri"
    elif int == 5:
        return "Sat"
    elif int == 6:
        return "Sun"

def month_of_year(int):
    if int == 1:
        return "Jan"
    elif int == 2:
        return "Feb"
    elif int == 3:
        return "Mar"
    elif int == 4:
        return "Apr"
    elif int == 5:
        return "May"
    elif int == 6:
        return "Jun"
    elif int == 7:
        return "Jul"
    elif int == 8:
        return "Aug"
    elif int == 9:
        return "Sep"
    elif int == 10:
        return "Oct"
    elif int == 11:
        return "Nov"
    elif int == 12:
        return "Dec"



def format_to_RFC822(dateobj):
    # "Wed, 02 Oct 2002 08:00:00 EST"
    parsed_date = dateutil.parser.parse(dateobj)
    dayofweek = day_of_week(parsed_date.weekday())
    day = str(parsed_date.day)
    month = month_of_year(parsed_date.month)
    year = str(parsed_date.year)
    time  = str(parsed_date.time())
    TZ = "GMT"


    Final = " ".join([dayofweek+",",day, month, year,time, TZ])

    return Final


