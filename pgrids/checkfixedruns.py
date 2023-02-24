import numpy as np
import matplotlib.pyplot as plt
from posydon.grids.psygrid import PSyGrid

"""
Returns percent of runs fixed between two files
"""

# read in the files being compared
grid1 = PSyGrid("lowmetal_wrlof.h5")
grid2 = PSyGrid("lowmetal_wrlof_rerun1.h5")

# get total number of runs per grid, and total not converged
IC_vals1 = [grid1[i].final_values['interpolation_class']
    if grid1[i].final_values is not None else np.nan
    for i in range(len(grid1.MESA_dirs))]
IC_vals2 = [grid2[i].final_values['interpolation_class']
    if grid2[i].final_values is not None else np.nan
    for i in range(len(grid2.MESA_dirs))]

total1 = len(IC_vals1)
total2 = len(IC_vals2)
nc1 = [index for index,item in enumerate(IC_vals1) if item == 'not_converged']
nc2 = [index for index,item in enumerate(IC_vals2) if item == 'not_converged']
total_nc1 = len(nc1)
total_nc2 = len(nc2)

# get percent fixed 
fixed = (total2-total_nc2)/total_nc1 * 100
print("Total number of runs in the original run:", total1)
print("Total number of not converged in original run:", total_nc1)
print("Percent fixed by rerun:", fixed,"%")
