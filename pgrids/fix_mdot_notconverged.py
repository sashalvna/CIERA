import numpy as np
import matplotlib.pyplot as plt
from posydon.grids.psygrid import PSyGrid

# read in the file
grid = PSyGrid("lowmetal.h5")
#grid = h5py.File("lowmetal.h5", 'r+')

# getting the index number for all crashed runs in the whole grid
IC_vals = [grid[i].final_values['interpolation_class']
    if grid[i].final_values is not None else np.nan
    for i in range(len(grid.MESA_dirs))]
notconverged_MT_index = [index for index,item in enumerate(IC_vals) if item == 'not_converged']

mdot_ind = []
for i in notconverged_MT_index:
    mdot = grid[i].binary_history['lg_mtransfer_rate'][-1]
    if mdot > -6:
        print(mdot)
        #grid[i].final_values['interpolation_class'] = 'unstable_MT'


   
    
