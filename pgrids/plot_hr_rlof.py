import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from posydon.grids.psygrid import PSyGrid
import pandas as pd
import matplotlib.patheffects as pe

# read in the file
grid = PSyGrid("zsolarwrlof_combined.h5")
m_COs = [0.9, 1.0, 1.1, 1.2, 1.3] #(10**np.linspace(np.log10(0.1), np.log10(0.9), 10)) #initial m2 values

#read in blue lurker data
bl = pd.read_csv('bluelurkers.csv')
bl_id = np.array(bl['WOCS_ID'][:4])
bl_Teff = np.array(bl['T_eff'][:4])
bl_logg = np.array(bl['log_g'][:4])
bl_err = np.array(bl['error'][:4])

# getting the index number for all stable and no MT runs in the grid
IC_vals = [grid[i].final_values['interpolation_class']
    if grid[i].final_values is not None else np.nan
    for i in range(len(grid.MESA_dirs))]
stable_MT_index = [index for index,item in enumerate(IC_vals) if item == 'stable_MT']
no_MT_index = [index for index,item in enumerate(IC_vals) if item == 'no_MT']

# among those not converged runs, read the final MT value for each run
f = []
for elems in stable_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    max_mdot = max(grid[elems].binary_history['lg_mtransfer_rate'])
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    p_final = grid[elems].binary_history['period_days'][-1]
    if p_final > 1000:
        continue
    p_orb = np.log10(grid[elems].binary_history['period_days'])
    wcrit = grid[elems].final_values['S2_surf_avg_omega_div_omega_crit']
    m2_final = grid[elems].final_values['star_2_mass']
    teff = grid[elems].history2['log_Teff']
    r = 10**(grid[elems].history2['log_R'])
    m2 = grid[elems].binary_history['star_2_mass']
    g = 6.67259E-8 * m2 * 1.989e33 / (r*6.95700e10)**2
    logg = np.log10(g)
    logL = grid[elems].history2['log_L']
    f.append([elems, m1_all, m2_all, p_all, mdot_all, wcrit, m2_final, logg, teff, logL, p_orb])
f = np.array(f)
f = np.transpose(f)

plt.figure(figsize=(5,5), dpi=300)
for m_CO in m_COs:
    #set min m2 value for island
    minm2 = m_CO + 0.01

    #get indices of all models in the WRLOF island
    ind = np.where(f[6] > minm2)[0]
    f = np.transpose(f)
    f1 = f[ind]
    f = np.transpose(f)
    f1 = np.transpose(f1)

    #get only indices of the slice
    ind1 = np.where((m_CO-0.02 < f1[2]) & (m_CO+0.02 > f1[2]))[0]
    f1 = np.transpose(f1)
    f2 = f1[ind1]

    f1 = np.transpose(f1)
    combined = np.concatenate(f[10]) #f1[10][:11])
    minp = min(combined)
    maxp = max(combined)

    #norm = mpl.colors.Normalize(vmin=minp, vmax=maxp)
    #cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.viridis)
    #cmap.set_array([])

    #fig, ax = plt.subplots(dpi=100)
    #for i in range(len(f2)):
    #    ax.plot(f2[i][8], f2[i][7], c=cmap.to_rgba(f2[i][10]))
    #fig.colorbar(cmap)
    
    print(len(f2))

    #plt.figure(figsize=(10, 10))
    for i in range(len(f2)):
        plt.scatter(f2[i][8], f2[i][7], c=f2[i][10], cmap='viridis', vmin=minp, vmax=maxp, s=10)
    #print(f2[1][1], f2[1][3])

    #plt.colorbar(orientation='horizontal', label=r'$P_{orb}$')
    #plt.clim(minp, maxp)

    if m_CO == 0.9:
        xmin = 3.83
        xmax = 3.7
        ymin = 4.6
        ymax = 3.9
    if m_CO == 1.0:
        xmin = 3.83
        xmax = 3.72
        ymin = 4.6
        ymax = 3.9
    if m_CO == 1.1:
        xmin = 3.88 
        xmax = 3.74 
        ymin = 4.6  
        ymax = 3.6 
    if m_CO == 1.2:
        xmin = 3.91
        xmax = 3.74
        ymin = 4.6
        ymax = 3.6
    if m_CO == 1.3:
        xmin = 3.91 
        xmax = 3.74
        ymin = 4.6
        ymax = 3.6
    xmin = 3.91
    xmax = 3.7
    ymin = 4.6
    ymax = 3.6

    plt.plot(np.log10(bl_Teff), bl_logg, 's', color='white', markersize=9)
    #plt.plot(np.log10(bl_Teff), bl_logg, 's', color='black', markersize=6)
    for i, txt in enumerate(bl_id):
        plt.annotate(txt, (np.log10(bl_Teff[i]), bl_logg[i]), color='black', textcoords='offset points', xytext=(3, 5), size=5, path_effects=[pe.withStroke(linewidth=4, foreground="white")])
    plt.errorbar(np.log10(bl_Teff), bl_logg, yerr=bl_err, fmt='s', color='white', elinewidth=4)
    plt.errorbar(np.log10(bl_Teff), bl_logg, yerr=bl_err, fmt='s', color='black', elinewidth=2)

    plt.rcParams["mathtext.fontset"] = 'cm'
    plt.xlabel(r'$\log$ $T_\mathrm{eff}$ $(\mathrm{K})$', fontsize=14)
    plt.ylabel(r'$\log$ $g$', fontsize=14)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    #plt.title(r'$M_2 = %.4s M_\odot$'%m_CO, fontsize=16)
plt.colorbar(orientation='horizontal', label=r'$\log$ $P_\mathrm{orb}$ $(\mathrm{days})$')
plt.clim(minp, maxp)
plt.savefig('zsolar_plots/rlof_hr_zsolarwrlof_lowp.png', bbox_inches='tight')
plt.show()
