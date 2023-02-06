# Before running this, one needs a `compute.txt` file.
# to get this run:
#   sacct --format User,ConsumedEnergy,CPUTime -S 2022-01-01T00:00:00 -E 2022-12-31T23:59:59 > compute.txt


import pandas as pd
import re

dat = pd.read_csv("compute.txt", delim_whitespace=True)

nans = dat.isna().any(axis=1)
dat[nans].shift(periods=1, axis="columns")
dat[nans] = dat[nans].shift(periods=1, axis="columns")
# if there are multiple NaNs in a row, need to shift again -> there should always be a time associated
nans = dat.loc[:, "CPUTime"].isna()
dat[nans].shift(periods=1, axis="columns")
dat[nans] = dat[nans].shift(periods=1, axis="columns")

def value_to_float(x):
    if x is None:
        return None
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    return 0.0

# converting energy consumed to a float with the fn above
dat['ConsumedEnergy'] = dat['ConsumedEnergy'].apply(value_to_float)
v = dat['CPUTime'][1:].str.split('-|:', expand=True)
no_days = v.isnull().any(axis=1)

# converting the date-time value to a readable number
# hh:mm:ss is default, but if there are clock-days, it will be d-hh:mm:ss
v[no_days] = v[no_days].shift(periods=1, axis='columns')
ln = v[no_days][0].shape[0]
v.loc[no_days, 0] = [0 for _ in range(ln)]
v = v.astype(int)

days, hours, minutes, seconds = v.sum()
minutes += seconds // 60
seconds = seconds % 60
hours += minutes // 60
minutes = minutes % 60
days += hours // 24
hours = hours % 24
print(f"Total CPUTime in core-time: {days}-{hours}:{minutes}:{seconds}")
core_hours = 24*days + hours + (minutes / 60) + (seconds / 3600)
print(f"Total CPUTime in core-hours: {core_hours}")

print(f"Consumed energy: {dat['ConsumedEnergy'].sum()}")

