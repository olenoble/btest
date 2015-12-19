import pandas as pd


def aj_df(x, y):
    if type(y) == pd.DataFrame:
        return y.apply(lambda z: z.asof(x.index))
    elif type(y) == pd.Series:
        return y.asof(x.index)
    else:
        return y


def aj(x, y):
    if type(y) == pd.DataFrame:
        return y.apply(lambda z: z.asof(x))
    elif type(y) == pd.Series:
        return y.asof(x)
    else:
        return y
