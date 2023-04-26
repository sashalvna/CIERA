import numpy as np
import os

"""
Writes grid.csv file for making grid of initial conditions for running POSYDON
"""

filename = 'gridslice_1_3.csv' #overwrites file, make sure to change name
m1 = 10**np.linspace(np.log10(0.7), np.log10(8.0), 20) #solar masses
m2 = [1.3] #10**np.linspace(np.log10(0.8), np.log10(1.3), 10) #solar masses
p = 10**np.linspace(np.log10(1e2), np.log10(200000), 20) #days

colnames = 'm1,m2,initial_period_in_days'
cols = [m1,m2,p]

with open(filename,'w') as file:
    file.write(colnames+'\n') 
    #for i in range(len(m1)): #all rows must have same number of columns (len(m1)=len(m2), etc)
    for i in range(len(m1)):
        for j in range(len(m2)):
            for k in range(len(p)):
                if m1[i]>=m2[j]: 
            	    rowval = "%s,%s,%s"%(m1[i],m2[j],p[k])
            	    file.write(rowval+'\n')
