from datetime import datetime, date, time, timedelta, tzinfo
from dateutil import parser
import numpy as np

## implement time series (from, to, step,... monthly, xth day of month, etc...)

def dateparse(x, american_convention=None, asdate=True):
    out = parser.parse(x, dayfirst=american_convention)
    return out.date() if asdate else out


def daystep(x, scaling=365, excludefirst=False, firstvalue=0.0):
    dt = [x.days / (1.0 * scaling) for x in np.diff(x)]
    return dt if excludefirst else [firstvalue] + dt
