# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 10:40:41 2020

@author: charb

Example 
for comet 9P/Tempel
r = 1.53
albedo = 0.04
Q = 6.8E+27  
A = 1.7E+08
f = 0.0056
f = activeFraction = getActiveFraction(r, Q, A, albedo)
print('f', f)

"""
# CometActiveFraction

import math

"""
The Correlation Between Visual Magnitudes and Water Production Rates
Jorda, L.; Crovisier, J.; Green, D. W. E.
Asteroids, Comets, Meteors 2008
LPI Contribution No. 1405, paper id. 8046
Pub Date: 2008 
Bibcode: 2008LPICo1405.8046J 
link: https://www.lpi.usra.edu/meetings/acm2008/pdf/8046.pdf
log Q[H2O] = 30.675 (0.007) – 0.2453 (0.0013) mH
"""
def getQH2OFromMagnitudeCorrelation(mH):
    return math.pow(10, 30.675 - 0.2453 * mH)

"""
P. R. Weisman mass-brightness relationship for new comets (1991)
log Mc = 20.0 - 0.4 log H10  -possible error
log Mc = 20.0 - 0.4 * H10  mass in grams
from a distribution of 256 long period comets compiled by Everhart 1967.
Page 313 Introduction to Comets by John C. Brandt and Robert D. Chapman 2nd Edition
Cambridge University Press, 2004
http://adsabs.harvard.edu/abs/2004inco.book.....B

Dynamical history of the Oort cloud
Authors:	 Weissman, Paul R.
Affiliation: AA(JPL, Pasadena, CA)
Publication: In: Comets in the post-Halley era. Vol. 1 (A93-13551 02-90), p. 463-486.  1991
Bibliographic Code:	1991ASSL..167..463W
http://adsabs.harvard.edu/abs/1991ASSL..167..463W

Title:	Intrinsic distributions of cometary perihelia and magnitudes
Authors:	Everhart, Edgar
Publication:	Astronomical Journal, Vol. 72, p. 1002 (1967) (AJ Homepage)
Publication Date:	10/1967
Origin:	ADS
DOI:	10.1086/110376
Bibliographic Code:	1967AJ.....72.1002E
http://adsabs.harvard.edu/abs/1967AJ.....72.1002E
"""
def getNewCometMass(h10):
    massGrams = math.pow(10, 20.0 - 0.4 * h10)
    return massGrams 


"""
        r^2 Q m L
f = ---------------------
      1368 A (1 - a)
	
r = heliocentric distance in AU
solar conststant S = 1368 watts/m^2
Q = water production rate in mol/sec
m = mW or mass of water molecule 3.0 x 10^-26 kg
L = 2.62 x 10^6 Joule/kg
A = area in m^2
a =  albedo
Comet 9P/Tempel 1: before and after impact
David W. Hughes
Monthly Notices of the Royal Astronomical Society, Volume 365, Issue 2, 11 January 2006, 
Pages 673–676, https://doi.org/10.1111/j.1365-2966.2005.09742.x
Published: 11 January 2006
for r = 1.53 AU, albedo = 0.04, Q = 6.8 x 10^27  A = 1.7 x 10^8, f = 0.0056
"""
def getActiveFraction(r, Q, A, albedo):
    m  = 3E-026
    S = 1368
    L = 2.62E+006 
    return (r * r * Q * m * L)/(S * A * (1 - albedo))


rn = 2000
area = 4*math.pi*rn*rn

# JPL Horizons ephemeris for 2020-Mar-20 
r = 1.686892344370
delta = 1.09209154734205

# Approximate total mag from recent COBS data by observers Maik Meyer and Carl Hergenrother
vmag = 8

mH = vmag - 5 * math.log10(delta)
print('heliocentric distance r ', r)
print('observer distance delta ', delta)
print('V magnitude', vmag)
print('heliocentric magnitude mH ', mH)
QH2O = getQH2OFromMagnitudeCorrelation(mH)

print('QH2O mol/s ', QH2O)

# JPL Horizons 
#    M1=  7.9      M2=  13.3     k1=  21.    k2=  5.      PHCOF=  .030           
h10 = 7.9
cometMassGrams = getNewCometMass(h10)
cometMassKG = cometMassGrams* 0.001

"""
The Rosetta blog (Emily Baldwin Senior Science Editor) 
preliminary science data on comet 67P/Churyumov-Gerasimenko October 3, 2014
Density	0.4 g/cm^3 = 400 kg/m^3
"""
density  = 400
volume = cometMassKG/density

albedo = 0.04
radius = math.pow((3 * volume / (4 * math.pi)),0.33333333)
area = 4 * math.pi * radius * radius
activeFraction = getActiveFraction(r, QH2O, area, albedo)
print('mass Kg', cometMassKG)
print('volume m^3', volume)
print('radius  m^2', radius)
print('activeFraction ', activeFraction)

