from datetime import datetime
import calendar



def calendar_workweeks():
    current_date_time = datetime.now()
    # %A = Day
    # %B = Month
    return {
        "month_name":current_date_time.strftime('%B'), 
        "month_int":current_date_time.month, "day_name":current_date_time.strftime('%A'),
        "day_int":current_date_time.weekday(),
        "date":current_date_time.date().isoformat()
    }


def calenday_days():
    return [("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday")]

def calenday_months():
    return  [("January", "January"), ("February", "February"), ("March", "March"), ("April", "April"), ("May", "May"), ("June", "June"), ("July", "July"), ("August", "August"), ("September", "September"), ("October", "October"), ("November", "November"), ("December", "December")]
