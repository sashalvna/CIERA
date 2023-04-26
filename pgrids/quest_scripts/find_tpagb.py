import numpy as np
import os
import glob

path = '/projects/b1119/sashalvna/zsolar'
path3 = path+'/zsolar_1_3/'
f = open('not_converged_zsolar_1_3.txt', 'r')
f2 = open('tpagb_check_zsolar_1_3.txt', 'w')

for line in f:
    dirname = '/m1_%s_m2_%s_initial_period_in_days_%s_grid_index*'%(line[:6],line[7:13],line[14:24])
    index = str(glob.glob(path3+dirname))
    dirname = index[34:-2] #34, 39
    os.chdir(path+dirname)
    flag=False
    try:
        with open('out.txt', 'r') as file:
            for line in (file.readlines() [-100:]):
                if 'Reached TPAGB' in line:
                    f2.write("True\n")
                    flag=True
                    break
                if flag==True:
                    break
            else:
                f2.write("False\n")
    except: 
        print(dirname)
        f2.write("None\n")
            
