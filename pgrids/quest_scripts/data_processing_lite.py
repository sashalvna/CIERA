import os
import sys
import numpy as np
from posydon.grids.psygrid import PSyGrid, DEFAULT_HISTORY_DS_EXCLUDE, DEFAULT_PROFILE_DS_EXCLUDE, EXTRA_COLS_DS_EXCLUDE
    
path = '/projects/b1119/sashalvna/nolim_zsolarwrlof/nolim_zsolarwrlof_0_9'
grid_name = "nolim_zsolarwrlof_0_9"

# choose the compression
grid_type = "LITE"

if grid_type == 'ORIGINAL':
    history_DS_error = None
    profile_DS_error = None
    history_DS_exclude = DEFAULT_HISTORY_DS_EXCLUDE
    profile_DS_exclude = DEFAULT_PROFILE_DS_EXCLUDE
elif grid_type == 'SMALL':
    history_DS_error = 0.01
    profile_DS_error = 0.01
    history_DS_exclude = EXTRA_COLS_DS_EXCLUDE+['surface_he4', 'surface_h1']
    profile_DS_exclude = EXTRA_COLS_DS_EXCLUDE+['surface_he4', 'surface_h1']
elif grid_type == 'LITE':
    history_DS_error = 0.1
    profile_DS_error = 0.1
    history_DS_exclude = EXTRA_COLS_DS_EXCLUDE
    profile_DS_exclude = EXTRA_COLS_DS_EXCLUDE
else:
    raise ValueError('grid_type = %s not supported!'%grid_type)
        
print('Creating psygrid for',grid_name, '...')
grid = PSyGrid(verbose=True)
#grid.create(path+"%s"%grid_name,
grid.create(path,path+grid_type+"/%s.h5"%grid_name,
            overwrite=True, history_DS_error=history_DS_error, profile_DS_error=profile_DS_error,
            history_DS_exclude=history_DS_exclude, profile_DS_exclude=profile_DS_exclude,
            compression="gzip9", start_at_RLO=False)
print('DONE!')
