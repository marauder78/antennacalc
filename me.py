import math
import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

bands = {
    80: {"min": 3500, "max": 3800, "harmonic": 0.125, "weight": 1},
    40: {"min": 7000, "max": 7200, "harmonic": 0.25, "weight": 2},
    20: {"min": 14000, "max": 14200, "harmonic": 0.5, "weight": 2},
    17: {"min": 18068, "max": 18168, "harmonic": 0.588, "weight": 0.3},
    15: {"min": 21000, "max":21450, "harmonic": 0.667, "weight": 0.1},
    10: {"min": 28000, "max": 29700, "harmonic": 1.0 ,"weight": 1},
    6: {"min": 50000, "max": 51000, "harmonic": 1.667, "weight": 0.1},
}



def electricalLen(fisicalLen, harmonic, KFactor):
    return ((300 * KFactor * harmonic) / float(fisicalLen)) * 100000

def loadDataFrame(startLen, stopLen, KFactor, step):
    result = []
    len = startLen
    
    while len < stopLen:
        distance = 0.0
        
        for band in bands:
            el = electricalLen(len, bands[band]["harmonic"], 0.96)
            bandCenter = (bands[band]["min"] + ((bands[band]["max"] - bands[band]["min"])/2.0))
            distanceFromCenter = abs(el - bandCenter) * bands[band]['weight']
            result.append({'length': len, 'band':band, 'resonance':el, 'bandCenter':bandCenter, 'bandLower': bands[band]["min"], 'bandUpper':bands[band]["max"], 'distanceFromCenter': distanceFromCenter})
        len += step

    return pd.DataFrame(result)

def loadCumulativeDataFrame(startLen, stopLen, KFactor, step):
    result = []
    len = startLen
    
    while len < stopLen:
        distance = 0.0
        
        for band in bands:
            el = electricalLen(len, bands[band]["harmonic"], 0.96)
            bandCenter = (bands[band]["min"] + ((bands[band]["max"] - bands[band]["min"])/2.0))
            distance += abs(el - bandCenter) * bands[band]['weight']

        result.append({'length': len, 'distance': distance})
        len += step

    return pd.DataFrame(result)




"""
#showing distance from bandCenter by length

df = loadDataFrame(600, 1200, 0.96, 1)
twentyMeters = df.loc[df['band']=="20"]

plt.plot(twentyMeters['length'], df.loc[df['band']=="10"]['distanceFromCenter'], 'c')
plt.plot(twentyMeters['length'], df.loc[df['band']=="20"]['distanceFromCenter'], 'm')
plt.plot(twentyMeters['length'], df.loc[df['band']=="40"]['distanceFromCenter'], 'y')
plt.plot(twentyMeters['length'], df.loc[df['band']=="80"]['distanceFromCenter'], 'k')

plt.plot(twentyMeters['length'], df.loc[df['band']=="15"]['distanceFromCenter'], 'r')
plt.plot(twentyMeters['length'], df.loc[df['band']=="17"]['distanceFromCenter'], 'b')
plt.plot(twentyMeters['length'], df.loc[df['band']=="50"]['distanceFromCenter'], 'g')
plt.show()

"""
df = loadCumulativeDataFrame(600, 1200, 0.96, 1)
plt.plot(df['length'], df['distance'], 'c')
#getting lowest distance
min = df.sort_values("distance").iloc[0]['length']
plt.xlabel("Minimo in {}".format(min))
plt.show()  #min @952



df = loadDataFrame(800, 1050, 0.96, 1)
print(df.loc[df['length']== min ].sort_values("band"))
