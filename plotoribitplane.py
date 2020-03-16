# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:56:54 2020

@author: charb
"""
import numpy as np
import math
import matplotlib.pyplot as plt

def getSemiMajorAxis(q, e):
    if (e == 1): 
        print("Error: parabolas have e = 1 and no semimajor axis")
        return -99
    # q  = a - ae = a (1-e)
    # a = q/(1 - e)
    return q/(1 - e)

# semi-parameter p is the distance from the focus 
# to the y-intercept of a conic section 
def getSemiParameter(q, e):
    p = 2*q
    if (e < 0):
        print("Error: negative eccentricity: " + e)
    elif (e < 1): 
        p = q * (1 + e)
    elif (e == 1):
        p = 2 * q
    elif (e > 1): 
        p = q * (1 + e)
    return p;

# values are for C/2019 Y1 (ATLAS)
# modify these values for your own orbit path
e = 0.996335
q = 0.837778 

semiparameter = getSemiParameter(q, e)
print('eccentricity e = ', e)
print('perihelion distance q = ', q)
print('semi-parameter p = ', semiparameter)


if (e < 1):
    a = getSemiMajorAxis(q, e)
    print('semi-major axis a = ', a, 'au')
    period = math.pow(a, 1.5)
    print('Period = ', period, 'years')


angles = np.linspace(-180,180,720)
if (e < 0.95):
    angles = np.linspace(-180,180,720)
elif (e < 1):
    angles = np.linspace(-170,170,720)

elif (e > 1):
    asymptote = np.math.degrees(  np.math.acos(-1/e))
    angles = np.linspace(5-asymptote,asymptote-5,721)
    print('asymptote = ', asymptote)

nu = np.radians(angles)

#r=nu
#r=np.cos(nu)
r=semiparameter/(1 + e * np.cos(nu))
x = r * np.cos(nu)
y = r * np.sin(nu)
    
plt.clf()

plt.plot(x, y, label='Orbit plane '+ 'q = ' + str(q) + 'e=' +str(e) , color='blue')
plt.arrow(0, 0, 10, 0, color='green')    # +x axis
plt.arrow(0, 0, -100, 0, color='orange') # -x axis
plt.arrow(0, 0, 0, 20, color='purple')   # +y axis
plt.arrow(0, 0, 0, -20, color='red')     # -y axis
plt.title('Comet Orbit Plane')
plt.grid(True)
plt.xlabel('x (au)')
plt.ylabel('y (au)')
# legend location rotates about +x axis
# 1 is upperright
# 2 is upperleft
# 3 is lowerleft
# 4 is lower right
plt.legend(loc=1)



plt.show()
