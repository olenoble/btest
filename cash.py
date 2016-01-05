import datetools
import tstools
import pandas as pd
import numpy as np


class CashAmount:

    defaut_start_date = datetools.dateparse('01-Jan-1970')

    def __init__(self):
        self.cash_value = pd.DataFrame()
        self.interest_rates = pd.DataFrame({'rate': 0.0}, index=[self.defaut_start_date])
        self.start_cash = 0
        self.daycount = 360

    def calculate_cash(self, daylist):
        self.interest_rates = tstools.aj(daylist, self.interest_rates)
        dayscaling = datetools.daystep(daylist, scaling=self.daycount, excludefirst=False, firstvalue=0.0)
        self.interest_rates['rate'] = self.interest_rates['rate'].shift().fillna(0.0) * dayscaling

        cash = self.start_cash * np.cumprod(self.interest_rates['rate'] + 1)

        self.cash_value = pd.DataFrame({'cash': cash}, index=daylist)

    def rescale_cash(self, dateof, new_value):
        val_ref = self.cash_value['cash'].asof(dateof)
        self.cash_value = self.cash_value / val_ref * new_value

