import numpy as np
import matplotlib.pyplot as plt
from posydon.grids.psygrid import PSyGrid

# read in the file
grid = PSyGrid("zsolarwrlof_1_2.h5")
#m_COs = (10**np.linspace(np.log10(0.1), np.log10(0.9), 10)) #initial m2 values
m_COs = [1.2]

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
tconditions = ['H-rich_Core_H_burning', 'H-rich_Core_He_burning','H-rich_Shell_H_burning', 'H-rich_Central_He_depleted','stripped_He_Core_He_burning', 'stripped_He_Central_He_depleted','H-rich_Central_C_depletion', 'stripped_He_Central_C_depletion', 'WD']
tnum = [0,1,2,3,4,5,6,7,8]
tcolor = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:olive', 'tab:cyan']

for elems in stable_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    m1_all = float(grid[elems].binary_history['star_1_mass'][0])
    m2_all = float(grid[elems].binary_history['star_2_mass'][0])
    p_all = float(grid[elems].binary_history['period_days'][0])
    flag1 = grid[elems].final_values['termination_flag_3']
    flag2 = grid[elems].final_values['termination_flag_4']
    for i in range(len(tconditions)):
        if flag1 == tconditions[i]:
            flag1 = tnum[i]
        if flag2 == tconditions[i]:
            flag2 = tnum[i]
    f1.append([elems,m1_all, m2_all, p_all, mdot_all, flag1, flag2])
f1 = np.array(f1)
f1 = np.transpose(f1)

for elems in unstable_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    flag1 = grid[elems].final_values['termination_flag_3']
    flag2 = grid[elems].final_values['termination_flag_4']
    for i in range(len(tconditions)):
        if flag1 == tconditions[i]:
            flag1 = tnum[i]
        if flag2 == tconditions[i]:
            flag2 = tnum[i]
    f2.append([elems, m1_all, m2_all, p_all, mdot_all, flag1, flag2])
f2 = np.array(f2)
f2 = np.transpose(f2)

for elems in no_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    flag1 = grid[elems].final_values['termination_flag_3']
    flag2 = grid[elems].final_values['termination_flag_4']
    for i in range(len(tconditions)):
        if flag1 == tconditions[i]:
            flag1 = tnum[i]
        if flag2 == tconditions[i]:
            flag2 = tnum[i]
    f3.append([elems, m1_all, m2_all, p_all, mdot_all, flag1, flag2])
f3 = np.array(f3)
f3 = np.transpose(f3)

for elems in notconverged_MT_index:
    mdot_all = grid[elems].binary_history['lg_mtransfer_rate'][-1]
    m1_all = grid[elems].binary_history['star_1_mass'][0]
    m2_all = grid[elems].binary_history['star_2_mass'][0]
    p_all = grid[elems].binary_history['period_days'][0]
    flag1 = grid[elems].final_values['termination_flag_3']
    flag2 = grid[elems].final_values['termination_flag_4']
    for i in range(len(tconditions)):
        if flag1 == tconditions[i]:
            flag1 = tnum[i]
        if flag2 == tconditions[i]:
            flag2 = tnum[i]
    f4.append([elems, m1_all, m2_all, p_all, mdot_all, flag1, flag2])

"""
#For finding not converged runs due to TPAGB
with open('not_converged_zsolarwrlof_1.txt', 'w') as f:
    for i in f4:
        line = "%s,%s,%s\n"%(np.format_float_positional(i[1],4, trim='k', unique=False),np.format_float_positional(i[2],4,trim='k',unique=False),np.format_float_scientific(i[3], precision=4, trim='k', unique=False))
        f.write(line)
"""

#For reading in runs that did not converge due to TPAGB
tpagb = []
with open('tpagb_check_zsolarwrlof_1_2.txt', 'r') as f:
    for line in f:
        if line=='True\n':
            tpagb.append(True)
        else:
            tpagb.append(False)
for i in range(len(f4)):
    f4[i].append(tpagb[i])
f4 = np.array(f4)
f4 = np.transpose(f4)


notconverged=0
for m_CO in m_COs:
    ind1 = np.where((m_CO-0.02 < f1[2]) & (m_CO+0.02 > f1[2]))[0]
    ind2 = np.where((m_CO-0.02 < f2[2]) & (m_CO+0.02 > f2[2]))[0]
    ind3 = np.where((m_CO-0.02 < f3[2]) & (m_CO+0.02 > f3[2]))[0]
    ind4 = np.where((m_CO-0.02 < f4[2]) & (m_CO+0.02 > f4[2]))[0]
   
    f11 = np.transpose(f1)
    f11 = f11[ind1]
    f11 = np.transpose(f11)
    f22 = np.transpose(f2)
    f22 = f22[ind2]
    f22 = np.transpose(f22)
    f33 = np.transpose(f3)
    f33 = f33[ind3]
    f33 = np.transpose(f33)
    f44 = np.transpose(f4)
    f44 = f44[ind4]
    f44 = np.transpose(f44)

    tpagb = []
    m6 = []
    nc = []
    for i in range(len(f44[4])):
        if f44[4][i] > -6:
            m6.append([f44[1][i], f44[3][i], f44[5][i], f44[6][i]])
        elif f44[7][i] == True:
            tpagb.append([f44[1][i], f44[3][i], f44[5][i], f44[6][i]])
        else:
            nc.append([f44[1][i], f44[3][i], f44[5][i], f44[6][i]])

    tpagb = np.array(tpagb)
    tpagb = np.transpose(tpagb)
    m6 = np.array(m6)
    m6 = np.transpose(m6)
    nc = np.array(nc)
    nc = np.transpose(nc)

    plt.figure(figsize=(5,10))

    try: plt.scatter(np.log10(f11[1]), np.log10(f11[3]),c= f11[6], vmin = 0, vmax = 7, marker='s', s=30, cmap='Dark2', label='Reached end life')
    except: pass
    try: plt.scatter(np.log10(f22[1]), np.log10(f22[3]),c= f22[6], vmin = 0, vmax = 7, marker='D', s=30, cmap='Dark2', label='Unstable RLOF')
    except: pass
    try: plt.scatter(np.log10(f33[1]), np.log10(f33[3]),c= f33[6], vmin = 0, vmax = 7, marker='s', s=30, cmap='Dark2')
    except: pass
    try: plt.scatter(np.log10(tpagb[0]), np.log10(tpagb[1]),c= tpagb[3], vmin = 0, vmax = 7, marker='*', s=40, cmap='Dark2', label='TPAGB')
    except: pass
    try: plt.scatter(np.log10(m6[0]), np.log10(m6[1]),c= m6[3], vmin = 0, vmax = 7, marker='D', s=30, cmap='Dark2')
    except: pass
    try: plt.scatter(np.log10(nc[0]), np.log10(nc[1]),c= nc[3], vmin = 0, vmax = 7, marker='X', s=30, cmap='Dark2', label='Not converged')
    except: pass
   
    plt.rcParams["mathtext.fontset"] = 'cm'
    plt.xlabel(r'$\log_{10}(M_1/M_\odot)$', fontsize=14)
    plt.ylabel(r'$\log_{10}(P_\mathrm{orb}/\mathrm{days})$', fontsize=14)
    plt.title(r'$M_2 = %.4s M_\odot$'%m_CO, fontsize=16)
    plt.colorbar(orientation='horizontal', label=r'$\mathrm{Termination Condition Star 2}$')
    plt.clim(0, 7)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.legend()

    plt.savefig('zsolarwrlof_m_CO_%.3s_m2_star2.png'%m_CO, bbox_inches='tight')
    plt.show()
    notconverged += len(nc)

print("Total number of runs:", len(IC_vals))
print("Total number not converged:", len(notconverged_MT_index))
print("Percent runs fixed:", (len(notconverged_MT_index)-notconverged)/len(notconverged_MT_index)*100)
