# -*- coding: utf-8 -*-
"""

    PlotJPLHorizonsEphemeris
    
    - queries JPL horizons with astroquery
    - save the quey as a fits table
    - reads the query results from fits table
    - extracts columns pertaining to comets 
    - converts date strings to Time objects 
         for use with matplotlib.dates as mdates
    - plots each selected column in a subplot
    - mdates share x-axis on each sub plot

Created on Sat Mar 21 07:41:24 2020
@author: Charles Bell
"""

import matplotlib.pyplot as plt
#https://astroquery.readthedocs.io/en/latest/
# from astroquery.jplhorizons import Horizons
from astropy.table import Table
from astropy.time import Time
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


"""
    2021-Jan-01 00:00 
    returns 2021-01-01 00:00:00.000
    which can be input to astropy.time.Time iso
    to plot dates with matplotlib 
"""
def getDateTimeUTHorizons(datestr):
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
    s = s + ' ' + hrs + ':' + mins +":00.000"
    return s

# uncomment the next three lines to query horizons and save the ephemeris to a fits table
# obj = Horizons(id='C/2019 Y4', location='500',epochs={'start':'2020-01-01', 'stop':'2021-01-01','step':'1d'} )
# eph = obj.ephemerides()
# eph.write('ephem.fits', format='fits', overwrite=True )


# assumes the ephemeris fits table has been saved 
# if you are modifying this demo code, you should only query the horisons server once
# and then use the file copy to modify to your needs.
eph = Table.read('ephem.fits')

objectname = eph.columns[eph.index_column('targetname')]
datetimestr = eph.columns[eph.index_column('datetime_str')]
jd = eph.columns[eph.index_column('datetime_jd')]
r = eph.columns[eph.index_column('r')]
delta = eph.columns[eph.index_column('delta')]
tmag = eph.columns[eph.index_column('Tmag')]
nmag = eph.columns[eph.index_column('Nmag')]
phase = eph.columns[eph.index_column('alpha')]
elong = eph.columns[eph.index_column('elong')]
psang = eph.columns[eph.index_column('sunTargetPA')]
psamv = eph.columns[eph.index_column('velocityPA')]
plang = eph.columns[eph.index_column('OrbPlaneAng')]
trueanomaly = eph.columns[eph.index_column('true_anom')]
ra = eph.columns[eph.index_column('RA')]
dec = eph.columns[eph.index_column('DEC')]
constellation = eph.columns[eph.index_column('constellation')]

datetimes = []
for datestr in datetimestr:
    datetimeUT = getDateTimeUTHorizons(datestr)
    dateTime = Time(datetimeUT, format='iso').datetime
    datetimes.append(dateTime)

fig, axs = plt.subplots(9, sharex=True, figsize=(20, 18))

fig.suptitle('JPL Horizons Ephemeris C/2019 Y4 (ATLAS)', x=0.50, y=0.91, fontsize=24)


locator = mdates.AutoDateLocator()
formatter = mdates.AutoDateFormatter(locator)
axs[0].xaxis.set_major_locator(locator)
axs[0].xaxis.set_major_formatter(formatter)
axs[1].xaxis.set_major_locator(locator)
axs[1].xaxis.set_major_formatter(formatter)
axs[2].xaxis.set_major_locator(locator)
axs[2].xaxis.set_major_formatter(formatter)
axs[3].xaxis.set_major_locator(locator)
axs[3].xaxis.set_major_formatter(formatter)
axs[4].xaxis.set_major_locator(locator)
axs[4].xaxis.set_major_formatter(formatter)
axs[5].xaxis.set_major_locator(locator)
axs[5].xaxis.set_major_formatter(formatter)
axs[6].xaxis.set_major_locator(locator)
axs[6].xaxis.set_major_formatter(formatter)
axs[7].xaxis.set_major_locator(locator)
axs[7].xaxis.set_major_formatter(formatter)
axs[8].xaxis.set_major_locator(locator)
axs[8].xaxis.set_major_formatter(formatter)


# plot magnitude plots with inverted y-axis
axs[0].invert_yaxis() # Total magnitude
axs[1].invert_yaxis() # Nuclear magnitude

# The x-axis formatted dates are shared in all plots
axs[8].set_xlabel('Date', fontsize=20)

axs[0].set_ylabel('Tmag', fontsize=20)
axs[1].set_ylabel('Nmag', fontsize=20)
axs[2].set_ylabel('r',    fontsize=20)
axs[3].set_ylabel('delta',fontsize=20)
axs[4].set_ylabel('Phase',fontsize=20)
axs[5].set_ylabel('Elong',fontsize=20)
axs[6].set_ylabel('PsAng',fontsize=20)
axs[7].set_ylabel('PsAMV',fontsize=20)
axs[8].set_ylabel('PlAng',fontsize=20)


axs[0].plot_date(datetimes, tmag,  '.', xdate=True, ydate = False)
axs[1].plot_date(datetimes, nmag,  '.', xdate=True, ydate = False)
axs[2].plot_date(datetimes, r,     '.', xdate=True, ydate = False)
axs[3].plot_date(datetimes, delta, '.', xdate=True, ydate = False)
axs[4].plot_date(datetimes, phase, '.', xdate=True, ydate = False)
axs[5].plot_date(datetimes, elong, '.', xdate=True, ydate = False)
axs[6].plot_date(datetimes, psang, '.', xdate=True, ydate = False)
axs[7].plot_date(datetimes, psamv, '.', xdate=True, ydate = False)
axs[8].plot_date(datetimes, plang, '.', xdate=True, ydate = False)

