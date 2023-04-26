import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec

"""
Plots HR diagram (log L vs log T_eff) and Mdot vs orbital period (and any additional plots) for a binary model.
"""

h = mr.MesaData('LOGS1_wrlof/history.data')
h2 = mr.MesaData('binary_history_wrlof.data')
h3 = mr.MesaData('LOGS2_wrlof/history.data')

print(h2.star_1_mass[0], h2.star_2_mass[0], h2.period_days[0])

#HR diagram with mass transfer indicated
mt =  np.where(10**(h2.lg_mstar_dot_1) > 10e-12)[0]
nomt = np.where(10**(h2.lg_mstar_dot_1) <= 10e-12)[0]
mt2 =  np.where(10**(h2.lg_mstar_dot_2) > 10e-12)[0]
nomt2 = np.where(10**(h2.lg_mstar_dot_1) <= 10e-12)[0]

print(h3.log_L)

for i in nomt:
    if i > mt[-1]:
        split = i
        break
    else:
        split = i
split = np.where(nomt == split)[0][0]

for i in nomt2:
    try:
        if i > mt2[-1]:
            split2 = i
            break
        else:
            split2 = i 
    except: 
        split2 = 1
split2 = np.where(nomt2 == split2)[0][0]

try:
    A = np.where(h3.log_L > 0.45)[0]
    A = np.where(h3.log_Teff == min(h3.log_Teff[A]))[0]

    B = np.where((h3.log_L > 0.3) & (3.785 < h3.log_Teff) & (h3.log_Teff < 3.79))[0]
    B = np.where(h3.log_L == min(h3.log_L[B]))[0]

    C = np.where(h3.log_L > 0.6)[0]
    C = np.where(h3.log_Teff == min(h3.log_Teff[C]))[0]

    D = np.where(h3.log_Teff == max(h3.log_Teff))[0]
except: pass

print(10**(h.log_Teff[0]), 10**(h.log_L[0]))
print(10**(h3.log_Teff[0]), 10**(h3.log_L[0]))
print(10**(h3.log_Teff[-1]), 10**(h3.log_L[-1]))
print(h.star_age[-1], h3.star_age[-1])
print(h2.star_1_mass[0], h2.star_1_mass[-1], (h2.star_1_mass[-1]- h2.star_1_mass[0]))
print(h2.star_2_mass[0], h2.star_2_mass[-1], (h2.star_2_mass[-1]- h2.star_2_mass[0]))

plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h.log_Teff[nomt[:split]], h.log_L[nomt[:split]], label=r'$\mathrm{Donor}$', color='tab:blue')
plt.plot(h.log_Teff[nomt[split:]], h.log_L[nomt[split:]], color='tab:blue')
plt.plot(h.log_Teff[mt], h.log_L[mt], label=r'$\mathrm{Donor, MT}$', linestyle='dashed', color='tab:blue')
plt.plot(h3.log_Teff[nomt2[:split2]], h3.log_L[nomt2[:split2]], label=r'$\mathrm{Accretor}$', color='tab:orange')
plt.plot(h3.log_Teff[nomt2[split2:]], h3.log_L[nomt2[split2:]], color='tab:orange')
plt.plot(h3.log_Teff[mt2], h3.log_L[mt2], label=r'$\mathrm{Accretor, MT}$', linestyle='dashed', color='tab:orange')

try:
    pointsx = [h3.log_Teff[A], h3.log_Teff[B], h3.log_Teff[C], h3.log_Teff[D]]
    pointsy = [h3.log_L[A], h3.log_L[B], h3.log_L[C], h3.log_L[D]]
    labels = ['D', 'C', 'B', 'A']
    plt.plot(pointsx, pointsy, '.', color='black')
    for i, txt in enumerate(pointsx):
        plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')
except: pass

plt.xlabel(r'$\log$ $T_\mathrm{eff}$ $(\mathrm{K})$', fontsize=14)
plt.ylabel(r'$\log$ $L$ $(L_\odot)$', fontsize=14)
plt.xlim(5.3, 3.2)
plt.legend()
plt.savefig('hr.png', bbox_inches='tight')
plt.show()


"""
#Mdot vs orbital period
plt.plot(h2.period_days, h2.lg_mstar_dot_1, label='Donor')
plt.plot(h2.period_days, h2.lg_mstar_dot_2, label='Accretor')
plt.xlabel('Orbital period (days)')
plt.ylabel('log M_dot')
plt.legend()
plt.show()
"""
#WRLOF efficiency
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, np.log10(h2.WRLOF_efficiency))

pointsx = [h2.period_days[A], h2.period_days[B], h2.period_days[C], h2.period_days[D]]
pointsy = [np.log10(h2.WRLOF_efficiency[A]), np.log10(h2.WRLOF_efficiency[B]), np.log10(h2.WRLOF_efficiency[C]), np.log10(h2.WRLOF_efficiency[D])]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\log_{10}$ $\beta_\mathrm{acc, WRLOF}$',fontsize=14)
plt.savefig('wrlofefficiency.png', bbox_inched='tight')
plt.show()

#Mdot vs orbital period, with wind
plt.figure(figsize=(8,6),dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, h2.lg_mstar_dot_1, label=r'$\dot{M}_\mathrm{d}$', color='tab:blue')
plt.plot(h2.period_days, h2.lg_mstar_dot_2, label=r'$\dot{M}_\mathrm{a}$', color='tab:orange')
plt.plot(h2.period_days, h2.lg_wind_mdot_1, label=r'$\dot{M}_\mathrm{d, wind}$', linestyle='dashed', color='tab:red')
plt.plot(h2.period_days, h2.lg_wind_mdot_2, label=r'$\dot{M}_\mathrm{a, wind}$', linestyle='dashed', color='tab:green')
#plt.plot(h2.period_days, h2.lg_mtransfer_rate, label='RLOF')

pointsx = [h2.period_days[A], h2.period_days[B], h2.period_days[C], h2.period_days[D]]
pointsy = [h2.lg_mstar_dot_2[A], h2.lg_mstar_dot_2[B], h2.lg_mstar_dot_2[C], h2.lg_mstar_dot_2[D]]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

pointsy = [h2.lg_wind_mdot_2[A], h2.lg_wind_mdot_2[B], h2.lg_wind_mdot_2[C], h2.lg_wind_mdot_2[D]]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')



plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\log_{10}$ $\dot{M}$ $(M_\odot/\mathrm{year})$', fontsize=14)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=4)
plt.savefig('mdotvsp.png', bbox_inches='tight')
plt.show()

"""
#Star age vs M dot
plt.plot(np.log10(max(h.star_age)-h.star_age), h2.lg_mstar_dot_1, label='Donor')
plt.plot(np.log10(max(h.star_age)-h.star_age), h2.lg_mstar_dot_2, label='Accretor')
plt.xlabel('log max star age - star age (years)')
plt.ylabel('log M_dot')
plt.legend()
plt.show()
"""

"""
#Mdots vs orbital period and M vs orbital period stacked
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6, 7))
fig.subplots_adjust(hspace=0)
ax[0].plot(h2.period_days, h2.lg_mstar_dot_1, label='Donor, total mass loss rate')
ax[0].plot(h2.period_days, h2.lg_mstar_dot_2, label='Accretor, total mass accretion rate', color='tab:orange')
ax[0].plot(h2.period_days, h2.lg_wind_mdot_1, label='Donor, wind mass loss rate', linestyle='--', color='tab:blue')
ax[0].plot(h2.period_days, h2.lg_wind_mdot_2, label='Accretor, wind mass loss rate', linestyle='--', color='tab:orange')
#ax[0].plot(h2.period_days, h2.lg_mtransfer_rate, label='RLOF')
ax[0].set_ylabel(r'log $M_{dot}$ ($M_\odot$/year)', fontsize=16)
ax[0].legend()
#ax[0].set_xlim([20000,25000])
#ax[0].set_ylim([-3.3, -3.1])

ax[1].plot(h2.period_days, h2.star_1_mass, label=r'Donor')
ax[1].plot(h2.period_days, h2.star_2_mass, label=r'Accretor',color='green')
ax[1].set_xlabel(r'Orbital period (days)',fontsize=16) 
ax[1].set_ylabel(r'Mass ($M_\odot$)', fontsize=16)
ax[1].legend()

plt.show()
"""
"""
#Radius vs orbital period
plt.plot(h2.period_days, h2.star_1_radius, label='Donor')
plt.plot(h2.period_days, h2.star_2_radius, label='Accretor')
plt.xlabel('Orbital period (days)')
plt.ylabel('Radius (Rsun)')
plt.legend()
plt.show()
"""
"""
#Radius vs time
plt.plot(h.star_age, h2.star_1_radius, label='Donor')
plt.plot(h.star_age, h2.star_2_radius, label='Accretor')
plt.xlabel('Star age (years)')
plt.ylabel('Radius (Rsun)')
#plt.xlim(2.4e8, 2.41e8)
plt.legend()
plt.show()
"""
#Rotational speed vs orbital period
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, h.surf_avg_omega_div_omega_crit, label='Donor')
plt.plot(h2.period_days, h3.surf_avg_omega_div_omega_crit, label='Accretor')
plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\omega/\omega_\mathrm{crit}$', fontsize=14)
plt.legend()
plt.savefig('wcrit.png', bbox_inches='tight')
plt.show()

#R_RL, R_star vs time
fig, ax1 = plt.subplots(figsize=(8, 6), dpi=100)
ax2 = ax1.twinx()
plt.rcParams["mathtext.fontset"] = 'cm'
ax1.plot(h2.period_days, np.log10(h2.rl_1), label=r'$R_{L,1}$', linestyle='dashed', color='tab:blue')
ax1.plot(h2.period_days, np.log10(h2.star_1_radius), label=r'$R_1$', color='tab:blue')
ax2.plot(h2.period_days, np.log10(h2.rl_2), label=r'$R_{L,2}$', linestyle='dashed', color='tab:orange')
ax2.plot(h2.period_days, np.log10(h2.star_2_radius), label=r'$R_2$', color='tab:orange')

pointsx = [h2.period_days[A], h2.period_days[B], h2.period_days[C], h2.period_days[D]]
pointsy = [np.log10(h2.star_2_radius[A]), np.log10(h2.star_2_radius[B]), np.log10(h2.star_2_radius[C]), np.log10(h2.star_2_radius[D])]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

pointsy = [np.log10(h2.rl_2[A]), np.log10(h2.rl_2[B]), np.log10(h2.rl_2[C]), np.log10(h2.rl_2[D])]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

pointsy = [np.log10(h2.star_1_radius[A]), np.log10(h2.star_1_radius[B]), np.log10(h2.star_1_radius[C]), np.log10(h2.star_1_radius[D])]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

ax1.set_xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
ax2.set_ylabel(r'$\log_{10}$ $R_1/R_{\odot,1}$',fontsize=14)
ax2.set_ylabel(r'$\log_{10}$ $R_2/R_{\odot,2}$',fontsize=14)
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.savefig('radius.png', bbox_inches='tight')
plt.show()

"""
#R_RL, R_star vs time
plt.plot(h.star_age[:-1], h2.rl_2, label='RL radius')
plt.plot(h.star_age[:-1], h2.star_2_radius, label='Accretor radius')
plt.xlabel('Star age (years)')
plt.ylabel('Radius (Rsun)')
#plt.xlim(7.23e8, 7.26e8)
plt.legend()
plt.show()
"""
"""
#He and C core mass vs time
plt.plot(h.star_age, h.he_core_mass, label='He core')
plt.plot(h.star_age, h.c_core_mass, label='C core')
plt.xlabel('Star age (years)')
plt.ylabel('Mass (Msun)')
plt.legend()
plt.show()
"""
#Mass vs orbital period
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, h2.star_1_mass, label=r'$\mathrm{Donor}$', color='tab:blue')
plt.plot(h2.period_days, h2.star_2_mass, label=r'$\mathrm{Accretor}$', color='tab:orange')

pointsx = [h2.period_days[A], h2.period_days[B], h2.period_days[C], h2.period_days[D]]
pointsy = [h2.star_2_mass[A], h2.star_2_mass[B], h2.star_2_mass[C], h2.star_2_mass[D]]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$M/M_\odot$', fontsize=14)
plt.legend()
plt.savefig('mvsp.png', bbox_inches='tight')
plt.show()

"""
#Time scales vs orbital period
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, h2.kh_timescale, label='Thermal timescale, donor', color='tab:blue')
plt.plot(h2.period_days, h.nuc_timescale, label='Nuclear timescale, donor', linestyle='dashed', color='tab:blue')
plt.plot(h2.period_days, h.mdot_timescale, label='Mass transfer timescale, donor', linestyle='dotted', color='tab:blue')
plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel('Timescale', fontsize=14)
plt.legend()
plt.savefig('timescales.png', bbox_inches='tight')
plt.show()
"""

#T_eff vs orbital period
fig, ax1 = plt.subplots(figsize=(8, 6), dpi=100)
ax2 = ax1.twinx()
plt.rcParams["mathtext.fontset"] = 'cm'
ax1.plot(h2.period_days, h.log_Teff, label=r'$\mathrm{Donor}$', color='tab:blue')
ax2.plot(h2.period_days, h3.log_Teff, label=r'$\mathrm{Accretor}$', color='tab:orange')

pointsx = [h2.period_days[A], h2.period_days[B], h2.period_days[C], h2.period_days[D]]
pointsy = [h3.log_Teff[A], h3.log_Teff[B], h3.log_Teff[C], h3.log_Teff[D]]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

ax1.set_xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
ax1.set_ylabel(r'$\log$ $T_{\mathrm{eff},1}$ $(\mathrm{K})$', fontsize=14)
ax2.set_ylabel(r'$\log$ $T_{\mathrm{eff},2}$ $(\mathrm{K})$', fontsize=14)
ax1.legend()
ax2.legend()
plt.savefig('teffvsp.png', bbox_inches='tight')
plt.show()

#Convection zones
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.fill_between(h2.period_days, h3.conv_mx1_bot, h3.conv_mx1_top, facecolor='tab:orange')

pointsx = [h2.period_days[A], h2.period_days[B], h2.period_days[C], h2.period_days[D]]
pointsy = [h3.conv_mx1_top[A], h3.conv_mx1_top[B], h3.conv_mx1_top[C], h3.conv_mx1_top[D]]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\mathrm{Mass}$ $\mathrm{fraction}$', fontsize=14)
plt.savefig('conv1.png', bbox_inches='tight')
plt.show()

plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.fill_between(h2.period_days, h3.conv_mx2_bot, h3.conv_mx2_top, facecolor='tab:orange')

pointsx = [h2.period_days[A], h2.period_days[B], h2.period_days[C], h2.period_days[D]]
pointsy = [h3.conv_mx2_top[A], h3.conv_mx2_top[B], h3.conv_mx2_top[C], h3.conv_mx2_top[D]]
labels = ['D', 'C', 'B', 'A']
plt.plot(pointsx, pointsy, '.', color='black')
for i, txt in enumerate(pointsx):
    plt.annotate(labels[i], (pointsx[i], pointsy[i]), color='black')

plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\mathrm{Mass}$ $\mathrm{fraction}$', fontsize=14)
plt.savefig('conv2.png', bbox_inches='tight')
plt.show()

#Luminosities vs orbital period
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, h.log_Lnuc, label=r'$\log$ $L_{nuc, 1}$', color='tab:blue')
plt.plot(h2.period_days, h.log_LH, label=r'$\log$ $L_{H, 1}$', linestyle='dashed', color='tab:red')
plt.plot(h2.period_days, h3.log_Lnuc, label=r'$\log$ $L_{nuc, 2}$', color='tab:orange')
plt.plot(h2.period_days, h3.log_LH, label=r'$\log$ $L_{H, 2}$', linestyle='dashed', color='tab:green')
plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\log$ $L$ $(L_\odot)$', fontsize=14)
plt.legend()
plt.savefig('luminosities.png', bbox_inches='tight')
plt.show()
