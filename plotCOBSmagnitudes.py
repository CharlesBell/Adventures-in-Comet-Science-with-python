# -*- coding: utf-8 -*-
"""
Created on Tue Mar  17 08:17:08 2020

@author: charb
"""

# plot COBS magnitudes

import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def getDateTimeUT(dateOfObservation):
    # print(dateOfObservation)
    yyyy = dateOfObservation[0:4]
    mm = dateOfObservation[5:7]
    dd = dateOfObservation[8:10]
    s = yyyy + '-' + mm + '-' + dd
    ff = float(dateOfObservation[10:13])
    seconds = int(ff * 86400)
    hrs = int(seconds/3600)
    mins = int((seconds - hrs * 3600)/60)
    secs = seconds  - hrs * 3600 - mins * 60
    s = s + ' '
    if (hrs < 10):
        s = s + "0"
    s = s + str(hrs) + ":"
    if (mins < 10):
        s = s + "0"
    s = s + str(mins) + ":"
    if (secs < 10):
        s = s + "0"
    s = s + str(secs)
    return s

datetimes = []
magnitudes = []

# COBS observation data can be found on line at https://cobs.si/
f = open('C2019 Y4 (ATLAS)-COBS-2020Mar17.txt', 'r')
for lines in f:
    if (lines.startswith('IIIYYYYMnL')):
        pass
    else:
        dateOfObservation = lines[11:26].strip()
        datetimeUT = getDateTimeUT(dateOfObservation)
        mag = lines[28:32].strip()
        # print(dateOfObservation, datetimeUT, mag)
        dateTime = Time(datetimeUT, format='iso').datetime
        datetimes.append(dateTime)
        magnitudes.append(float(mag))
 
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16
        }

boxprops = dict(boxstyle='round', facecolor='#ffffff', ec='#CCCCCC', alpha=0.9)
credittext = 'Credit: COBS Comet Observation Database \n       CC BY-NA-SA 4.0  https://cobs.si/'

fig, ax = plt.subplots(figsize=(20, 13))
locator = mdates.AutoDateLocator()
formatter = mdates.AutoDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

ax.grid(b=True, which='major', axis='both')
ax.set_title('COBS Magnitude Data Comet C/2019 Y4 (ATLAS)', fontdict=font)

if (len(magnitudes) > 0):
    ax.plot_date(datetimes, magnitudes, label='C/2019 Y4 magnitude', xdate=True, ydate=False)
    plt.text('2020-02-15', 17, credittext, fontdict=font, bbox=boxprops)

plt.xlabel('Date')
plt.gca().invert_yaxis()
plt.ylabel('Magnitude')
ax.legend(loc=1)
plt.show()
