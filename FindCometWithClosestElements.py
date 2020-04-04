# -*- coding: utf-8 -*-
"""
FindCometWithClosestElements.py

Created on Fri Apr  3 16:57:33 2020

@author: charb
"""
import math

desig = 'C/2019 Y4'
nameref = ''
qref = 0
eref = 0
iref = 0
periref = 0
noderef = 0

mindistance  = 10000000000
mincometname = ''
mincometname = 0 
mincometq = 0 
mincomete = 0 
mincometi = 0
mincometperi = 0 
mincometnode = 0 

# The file ELEMENTS.COMET  is on line https://ssd.jpl.nasa.gov/?sb_elem
# direct link:  https://ssd.jpl.nasa.gov/dat/ELEMENTS.COMET

file = open('ELEMENTS.COMET', 'r')
found = False
for lines in file:
    # print(lines)
    if ((desig in lines) == True):
        # print(lines)
        nameref = lines[0:44].strip()
        qref = float(lines[52:64].strip())
        eref = float(lines[64:75].strip())
        iref = float(lines[75:85].strip())
        periref = float(lines[85:95].strip())
        noderef = float(lines[95:105].strip())
        print('found elements for', desig)
        # print(nameref, qref,eref,iref, periref, noderef)
        found = True
        break
if (found == False):
    print(' elements for', desig, 'not found')
else:
    
    f = open('ELEMENTS.COMET', 'r')
    for lines in f:
        #print(lines)
        if (lines.startswith('Num') or lines.startswith('---')):
            pass
        elif ((desig in lines) == True):
            pass
        else:
            name = lines[0:44].strip()
            q = float(lines[52:64].strip())
            e = float(lines[64:75].strip())
            i = float(lines[75:85].strip())
            peri = float(lines[85:95].strip())
            node= float(lines[95:105].strip())
            qdiff = qref-q
            ediff = eref-e
            idiff = iref-i
            peridiff = periref-peri
            nodediff = noderef-node
            if (idiff > 180):
                idiff = 360 + i - iref
            if (peridiff > 180):
                peridiff = 360 + peri - periref
            if (nodediff > 180):
                nodediff = 360 + node - noderef
            # Euclidian distance in q, e, i, peri, node space
            distance = math.sqrt( (qdiff*qdiff) +(ediff*ediff) +(idiff*idiff) + (peridiff*peridiff) + (nodediff*nodediff))

            if (distance < mindistance):
                mindistance = distance
                mincometname = name 
                mincometq = q 
                mincomete = e 
                mincometi = i 
                mincometperi = peri 
                mincometnode = node 
    print('Reference comet')  
    print(nameref, 'q:', qref, 'e:', eref, 'i:', iref, 'peri:', periref, 'node:', noderef)   
    print('Closest neighbor comet')     
    print(mincometname, 'q:', mincometq, 'e:', mincomete, 'i:', mincometi, 'peri:', mincometperi, 'node:', mincometnode)   
    x = (qref-mincometq)*(qref-mincometq) +     (eref-mincomete)*(eref-mincomete) + (iref-mincometi)*(iref-mincometi) + (periref-mincometperi)*(periref-mincometperi) +(noderef-mincometnode)*(noderef-mincometnode)
    print('Minimum Euclidian distance (q, e, i, peri, node):', mindistance)     
    if (mindistance > 2):
        print('Large distance, probably not a good match')     

