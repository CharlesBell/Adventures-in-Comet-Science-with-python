# -*- coding: utf-8 -*-
"""

    plotCometC2019Y4MagEstimates
    
    - queries JPL horizons with astroquery
    - save the quey as a fits table
    - reads the query results from fits table
    - extracts columns pertaining to comets 
    - converts date strings to Time objects 
         for use with matplotlib.dates as mdates
    - extract and plots JPL Horizons Tmag and Nmag values
    - calculates and plots magnitudes for MPC, Yoshida, Nakano, and COBS brightness models
    - plots COBS observation data
    - plots Minor Planet Center observation data by magnitude band

Updated on 2020-Mar-23
@author: Charles Bell
"""

# 

#horizons
#https://astroquery.readthedocs.io/en/latest/
from astroquery.jplhorizons import Horizons
from astropy.table import Table
import matplotlib.pyplot as plt
from astropy.time import Time
import math
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def getDateTimeUTHorizons(datestr):
    #2021-Jan-01 00:00
    yyyy = datestr[0:4]
    mm = datestr[5:8]
    if (mm == 'Jan'):
        mm = '01'
    if (mm == 'Feb'):
        mm = '02'
    if (mm == 'Mar'):
        mm = '03'
    if (mm == 'Apr'):
        mm = '04'
    if (mm == 'May'):
        mm = '05'
    if (mm == 'Jun'):
        mm = '06'
    if (mm == 'Jul'):
        mm = '07'
    if (mm == 'Aug'):
        mm = '08'
    if (mm == 'Sep'):
        mm = '09'
    if (mm == 'Oct'):
        mm = '10'
    if (mm == 'Nov'):
        mm = '11'
    if (mm == 'Dec'):
        mm = '12'
    dd = datestr[9:11]
    s = yyyy + '-' + mm + '-' + dd
    hrs = datestr[12:14]
    mins = datestr[15:17]
    s = s + ' ' + hrs + ':' + mins +":00"
    return s

def getDateTimeUTCOBS(dateOfObservation):
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

def getDateTimeUTMPC(dateOfObservation):
    yyyy = dateOfObservation[0:4]
    mm = dateOfObservation[5:7]
    dd = dateOfObservation[8:10]
    s = yyyy + '-' + mm + '-' + dd
    ff = float(dateOfObservation[10: ])
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

cobsdatetimes = []
cobsobsmags = []

# COBS observation data can be found on line at https://cobs.si/
f = open('C2019 Y4 (ATLAS)-COBS-2020Mar22.txt', 'r')
for lines in f:
    if (lines.startswith('IIIYYYYMnL')):
        pass
    else:
        dateOfObservation = lines[11:26].strip()
        datetimeUT = getDateTimeUTCOBS(dateOfObservation)
        mag = lines[28:32].strip()
        # print(dateOfObservation, datetimeUT, mag)
        dateTime = Time(datetimeUT, format='iso').datetime
        cobsdatetimes.append(dateTime)
        cobsobsmags.append(float(mag))

#MPC observations
f2 = open('D:\\Comets and Asteroids\\C2019 Y4 (ATLAS)\\C_2019_Y4.txt', "r")
MPCm1dates = []
MPCm1mags = []

MPCm2dates = []
MPCm2mags = []

MPCRdates = []
MPCRmags = []

MPCVdates = []
MPCVmags = []

MPCGdates = []
MPCGmags = []

for lines in f2:
    packed = lines[0:12].strip()
    orbitType = lines[4:5].strip()
    typeOfObservation = lines[14:15].strip()
    year = int(lines[15:19])
    # print(lines)

        
    if ((typeOfObservation != 's') and (typeOfObservation != 'S')):        
        dateOfObservation = lines[15:32].strip()
        # print('dateOfObservation', dateOfObservation)
        datetimeUT = getDateTimeUTMPC(dateOfObservation)
        # print('datetimeUT', datetimeUT)
        dt = Time(datetimeUT, format='iso').datetime
        # print('dt', dt)
        #mpcdates.append(dt)
        observedRA = lines[32:44].strip()
        observedDecl = lines[44:56].strip()
        observedMagnitude = lines[65:70].strip(' ')
        #observedMagnitude = lines[65:70]
        #print('observedMagnitude', observedMagnitude)
        magnitudeBand = lines[70:71].strip()
        observatoryCode = lines[77:80].strip();
        reference = lines[72:77].strip();
        if   ((len(observedMagnitude) > 0) and (magnitudeBand == "N")):
            MPCm2dates.append(dt)
            MPCm2mags.append(float(observedMagnitude))
        elif ((len(observedMagnitude) > 0) and (magnitudeBand == "T")):
            MPCm1dates.append(dt)
            MPCm1mags.append(float(observedMagnitude))
        elif ((len(observedMagnitude) > 0) and (magnitudeBand == "R")):
            MPCRdates.append(dt)
            MPCRmags.append(float(observedMagnitude))
        elif ((len(observedMagnitude) > 0) and (magnitudeBand == "V")):
            MPCVdates.append(dt)
            MPCVmags.append(float(observedMagnitude))
        elif ((len(observedMagnitude) > 0) and (magnitudeBand == "G")):
            MPCGdates.append(dt)
            MPCGmags.append(float(observedMagnitude))

# Geocentric [500]
# obj = Horizons(id='C/2019 Y4', location='500',epochs={'start':'2019-12-28', 'stop':'2021-01-01','step':'1d'} )
# eph = obj.ephemerides()
# eph.write('ephem.fits', format='fits', overwrite=True )

eph = Table.read('ephem.fits')
datetime_str = eph.columns[eph.index_column('datetime_str')]
jd = eph.columns[eph.index_column('datetime_jd')]
r = eph.columns[eph.index_column('r')]
delta = eph.columns[eph.index_column('delta')]
phase = eph.columns[eph.index_column('alpha')]

TP= 2459000.51510898
datetimes = []
jplTmags = []
jplNmags = []
mpcmags = []
yoshidamags = []
cobsdates = []
cobsmags = []
nakanodates = []
nakanomags = []
for datestr in datetime_str:
    datetimeUT = getDateTimeUTHorizons(datestr)
    dateTime = Time(datetimeUT, format='iso').datetime
    datetimes.append(dateTime)
    
i = 0
while (i < len(datetimes)):
    mpcmags.append(6    + 5 * math.log10(delta[i]) + 2.5 * 4  * math.log10(r[i]))
    jplTmags.append(7.9  + 5 * math.log10(delta[i]) + 21  * math.log10(r[i]))            
    jplNmags.append(13.3 + 5 * math.log10(delta[i]) + 5.   * math.log10(r[i]) + .030*phase[i])
    yoshidamag =    -0.5 + 5 * math.log10(delta[i]) + 36   * math.log10(r[i])
    if (jd[i] > TP-73):
        yoshidamag  = 5.5 + 5 * math.log10(delta[i]) + 10  * math.log10(r[i])
    yoshidamags.append(yoshidamag)
    if ((jd[i] < (TP - 70))):
        cobsdates.append(datetimes[i])
        cobsmags.append(-1.62 + 5 * math.log10(delta[i]) + 2.5 * 16.94   * math.log10(r[i]))
    if ((jd[i] > (TP-30)) and (jd[i] < (TP+31))):
        nakanodates.append(datetimes[i])
        nakanomags.append(5.5 + 5 * math.log10(delta[i]) + 10 * math.log10(r[i]))
        
    i = i + 1

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }

boxprops = dict(boxstyle='round', facecolor='#ffffff', ec='#CCCCCC', alpha=0.9)

observers = 'Observers: Christian Harder, Timo Karhula, Maciej Kwinta, \nPiotr Guzik, Maciej Reszelski, Nick James, Denis Buczynski,  \nPiotr Nowak, Maik Meyer, Sandor Szabo, Kevin Hills,\n Teerasak Thaluang, Carl Hergenrother, Carlos Labordena, \nMariusz Swietnicki, Juan Jose Gonzalez Suarez, Jerzy Bohusz, \nArtyom Novichonok, Steffen Fritsche, Uwe Pilz,Alex Scholten, \nThomas Lehmann, Jose Pablo Navarro Pina, David Swan, \nJohan Warell, Nirmal Paul, Pieter-Jan Dekelver,\nMartin Masek, Gideon van Buitenen'
credittext = 'Credit: COBS Comet Observation Database – CC BY-NA-SA 4.0\n'

fig, ax = plt.subplots(figsize=(20, 13))

locator = mdates.AutoDateLocator()
formatter = mdates.AutoDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

ax.grid(b=True, which='major', axis='both')
ax.set_title('Comet C/2019 Y4 (ATLAS) Magnitude Estimates (2020-Mar-22) ', fontsize=24)

# plt.text('2020-07-15', -5, observers, fontdict=font, bbox=boxprops)
# plt.text('2020-04-01', 24, credittext, fontdict=font, bbox=boxprops)

ax.plot_date(datetimes, mpcmags, '.', label='MPC M1 mag H0=6 n=4', xdate=True, ydate = False)
ax.plot_date(datetimes, jplTmags,'.', label='JPL Horizons T-mag H0=7.7 n=5.4', xdate=True, ydate = False)
ax.plot_date(datetimes, jplNmags, '.',label='JPL Horizons N-mag H0=13.3 n=1.25  phcoeff=0.030', xdate=True, ydate = False)
ax.plot_date(datetimes, yoshidamags,'.', label='S. Yoshida Total mag H0=-0.5 n=14.4; H0=5.5 n=4',  xdate=True, ydate = False)
ax.plot_date(cobsdatetimes, cobsobsmags, '*', label='COBS observed mag', xdate=True, ydate=False)
ax.plot_date(cobsdates, cobsmags,  '.', label='COBS mag H0=-1.62 n=16.94', xdate=True, ydate = False)
ax.plot_date(nakanodates, nakanomags, '.',  label='NAKANO mag H0=-5.5 n=4 ', xdate=True, ydate = False)
ax.plot_date(MPCm1dates, MPCm1mags, '^',  label='MPC observed m1 mag', xdate=True, ydate = False)
ax.plot_date(MPCm2dates, MPCm2mags, 'v', label='MPC observed m2 mag', xdate=True, ydate = False)
ax.plot_date(MPCRdates, MPCRmags, '.',  label='MPC observed R mag', xdate=True, ydate = False)
ax.plot_date(MPCVdates, MPCVmags, '.',  label='MPC observed V mag', xdate=True, ydate = False)
ax.plot_date(MPCGdates, MPCGmags, '.',  label='MPC observed G mag', xdate=True, ydate = False)
plt.xlabel('Date', fontsize=20)
plt.gca().invert_yaxis()
plt.ylabel('Magnitude', fontsize=20)
ax.legend(loc=1)
plt.show()
