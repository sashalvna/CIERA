import numpy as np
import matplotlib.pyplot as plt
from posydon.grids.psygrid import PSyGrid

#grid = PSyGrid("CO-HMS_RLO_post_processed_grid_combined_with_rerun.h5")
grid = PSyGrid("lowmetal_r1.h5")
m_COs = (10**np.linspace(np.log10(0.1), np.log10(0.9), 10)) #np.unique(np.around(grid.initial_values['star_2_mass'],1))
#m_COs_centers = 10**(np.log10(np.array(m_COs)[:-1])+(np.log10(np.array(m_COs)[1:])-np.log10(np.array(m_COs)[:-1]))/2)
#m_COs_centers = [0.]+m_COs_centers.tolist()+[50.]

for k, m_CO in enumerate(m_COs):
        
    PLOT_PROPERTIES = {
        'figsize' : (3.38, 6),
        'show_fig' : False,
        'close_fig' : True,
        'path_to_file': './',
        'fname': 'm_CO_%1.1f_lowmetal.png'%m_CO,
        'title' : r'$M_2 = %2.2f M_\odot$'%m_CO,
        'log10_x' : True,
        'log10_y' : True,
        'zmin' : m_CO-0.02,
        'zmax' : m_CO+0.08,
        'legend2D' : {
            'title' : '$\mathrm{mass\,transfer\,cases}$',
            'bbox_to_anchor' : (1.03, 0.5)},
            'marker_size': 5,
    }

    m2 = [grid[i].final_values['star_2_mass']
        if grid[i].final_values is not None else np.nan
        for i in range(len(grid.MESA_dirs))]
    m2 = np.array(m2)


    fig = grid.plot2D('star_1_mass', 'period_days', m2,
                 termination_flag= 'termination_flag_1',
                 grid_3D=True, slice_3D_var_str='star_2_mass',
                 slice_3D_var_range=(m_CO-0.05,m_CO+0.05),
                 verbose=False, **PLOT_PROPERTIES)

                 
