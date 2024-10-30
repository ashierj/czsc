import numpy as np
import talib
from talib import MA_Type

close = np.random.random(100)
output = talib.SMA(close)

print(output)

upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)

output = talib.MOM(close, timeperiod=5)