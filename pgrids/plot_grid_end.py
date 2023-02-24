import numpy as np
import matplotlib.pyplot as plt
from posydon.grids.psygrid import PSyGrid

# read in the file
grid = PSyGrid("z_low_wrlof_combined2.h5")
#m_COs = (10**np.linspace(np.log10(0.1), np.log10(0.9), 10)) #initial m2 values
m_COs = [0.9, 1.0, 1.1]

# getting the index number for all crashed runs in the whole grid
IC_vals = [grid[i].final_values['interpolation_class']
    if grid[i].final_values is not None else np.nan
    for i in range(len(grid.MESA_dirs))]
stable_MT_index = [index for index,item in enumerate(IC_vals) if item == 'stable_MT']
unstable_MT_index = [index for index,item in enumerate(IC_vals) if item == 'unstable_MT']
no_MT_index = [index for index,item in enumerate(IC_vals) if item == 'no_MT']
notconverged_MT_index = [index for index,item in enumerate(IC_vals) if item == 'not_converged']

# among those not converged runs, read the final MT value for each run
f1 = []
f2 = []
f3 = []
f4 = []
for elems in stable_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    max_mdot = max(grid[elems].binary_history['lg_mtransfer_rate'])
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    f1.append([elems, m1_all, m2_all, p_all, mdot_all])
f1 = np.array(f1)
f1 = np.transpose(f1)

for elems in unstable_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    max_mdot = max(grid[elems].binary_history['lg_mtransfer_rate'])
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    f2.append([elems, m1_all, m2_all, p_all, mdot_all])
f2 = np.array(f2)
f2 = np.transpose(f2)

for elems in no_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    max_mdot = max(grid[elems].binary_history['lg_mtransfer_rate'])
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    f3.append([elems, m1_all, m2_all, p_all, mdot_all])
f3 = np.array(f3)
f3 = np.transpose(f3)

for elems in notconverged_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    max_mdot = max(grid[elems].binary_history['lg_mtransfer_rate'])
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    wcrit = grid[elems].final_values['S2_surf_avg_omega_div_omega_crit']
    term = grid[elems].final_values[-5]
    if term == 'min_timestep_limit':
        term = 1
    else:
        term = 0
    f4.append([elems, m1_all, m2_all, p_all, mdot_all, wcrit, term])

"""
with open('not_converged_zsolar_1_2.txt', 'w') as f:
    for i in f4:
        line = "%s,%s,%s\n"%(np.format_float_positional(i[1],4, trim='k', unique=False),np.format_float_positional(i[2],4,trim='k',unique=False),np.format_float_scientific(i[3], precision=4, trim='k', unique=False))
        f.write(line)
"""
"""
#For reading in runs that did not converge due to TPAGB
tpagb = []
with open('tpagb_check_zsolar.txt', 'r') as f:
    for line in f:
        if line=='True\n':
            tpagb.append(True)
        else:
            tpagb.append(False)
for i in range(len(f4)):
    f4[i].append(tpagb[i])
"""
f4 = np.array(f4)
f4 = np.transpose(f4)


notconverged=0
tpagb_count=0
for m_CO in m_COs:
    ind1 = np.where((m_CO-0.02 < f1[2]) & (m_CO+0.02 > f1[2]))[0]
    ind2 = np.where((m_CO-0.02 < f2[2]) & (m_CO+0.02 > f2[2]))[0]
    ind3 = np.where((m_CO-0.02 < f3[2]) & (m_CO+0.02 > f3[2]))[0]
    ind4 = np.where((m_CO-0.02 < f4[2]) & (m_CO+0.02 > f4[2]))[0]
    
    #tpagb = []
    mintimestep = []
    m6 = []
    nc = []
    for i in range(len(f4[4][ind4])):
        if f4[4][ind4][i] > -6:
            m6.append([f4[1][ind4][i], f4[3][ind4][i]])
        #elif (f4[7][ind4][i] == True) & (f4[6][ind4][i] == 1):
        #    mintimestep.append([f4[1][ind4][i], f4[3][ind4][i]])
        #elif f4[7][ind4][i] == True:
        #    tpagb.append([f4[1][ind4][i], f4[3][ind4][i]])
        else:
            nc.append([f4[1][ind4][i], f4[3][ind4][i]])

    #tpagb = np.array(tpagb)
    #tpagb = np.transpose(tpagb)
    mintimestep = np.array(mintimestep)
    mintimestep = np.transpose(mintimestep)
    m6 = np.array(m6)
    m6 = np.transpose(m6)
    nc = np.array(nc)
    nc = np.transpose(nc)

    plt.figure(figsize=(5,8))

    plt.scatter(np.log10(f1[1][ind1]), np.log10(f1[3][ind1]), marker='s', s=30, color='tab:blue', label='Stable RLOF')
    plt.scatter(np.log10(f2[1][ind2]), np.log10(f2[3][ind2]), marker='D', s=30, color='tab:orange', label='Unstable RLOF')
    plt.scatter(np.log10(f3[1][ind3]), np.log10(f3[3][ind3]), marker='s', s=30, color='lightgray', label='No RLOF')
    #try: plt.scatter(np.log10(tpagb[0]), np.log10(tpagb[1]), marker='*', s=40, color='tab:green', label='Reached TPAGB')
    #except: pass
    #try: plt.scatter(np.log10(mintimestep[0]), np.log10(mintimestep[1]), marker='*', s=20, color='gold', label='Min timestep limit')
    #except: pass
    try: plt.scatter(np.log10(m6[0]), np.log10(m6[1]), marker='D', s=30, color='tab:orange')
    except: pass
    try: plt.scatter(np.log10(nc[0]), np.log10(nc[1]), marker='X', s=30, color='tab:red', label='Not converged')
    except: pass
   
    plt.rcParams["mathtext.fontset"] = 'cm'
    plt.xlabel(r'$\log_{10}(M_1/M_\odot)$', fontsize=14)
    plt.ylabel(r'$\log_{10}(P_\mathrm{orb}/\mathrm{days})$', fontsize=14)
    plt.title(r'$M_2 = %.4s M_\odot$'%m_CO, fontsize=16)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.legend()

    plt.savefig('z_low_plots/z_low_wrlof_m_CO_%.3s_m2_endcondition.png'%m_CO, bbox_inches='tight')
    plt.show()
    notconverged += len(nc[0])
    #tpagb_count += len(tpagb[0])

print("Total number of runs:", len(IC_vals))
print("Total number not converged:", len(notconverged_MT_index))
print("Total number remaining not converged:", notconverged)
#print("Total TPAGB:", tpagb_count)
print("Percent runs fixed:", (len(notconverged_MT_index)-notconverged)/len(notconverged_MT_index)*100)

