print('Import modules')
import datetools
import tstools
import cash
#import underlying
#import basket
#import weight


from datetime import timedelta
import pandas as pd

print('Calculate time series')
#start_date = parser.parse("12/04/2014", dayfirst=None).date()
start_date = datetools.dateparse('2014-04-12')

x = [start_date + timedelta(i) for i in range(100)]
y = [start_date + timedelta(2 * i) for i in range(100)]

ratets = pd.DataFrame({'rate': 0.1}, index=x)

c = cash.CashAmount()
c.start_cash = 100
c.interest_rates = ratets
c.calculate_cash(y)

print((c.cash_value))

rescale_date = datetools.dateparse('2014-05-01')
c.rescale_cash(rescale_date, 100)
print((c.cash_value))
