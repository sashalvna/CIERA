import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec

"""
Plots HR diagram (log L vs log T_eff) and Mdot vs orbital period (and any additional plots) for a binary model.
"""

h = mr.MesaData('LOGS1_nowrlof/history.data')
h2 = mr.MesaData('binary_history_nowrlof.data')
h3 = mr.MesaData('LOGS2_nowrlof/history.data')

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

plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h.log_Teff[nomt[:split]], h.log_L[nomt[:split]], label=r'$\mathrm{Donor}$', color='tab:blue')
plt.plot(h.log_Teff[nomt[split:]], h.log_L[nomt[split:]], color='tab:blue')
plt.plot(h.log_Teff[mt], h.log_L[mt], label=r'$\mathrm{Donor, MT}$', linestyle='dashed', color='tab:blue')
plt.plot(h3.log_Teff[nomt2[:split2]], h3.log_L[nomt2[:split2]], label=r'$\mathrm{Accretor}$', color='tab:orange')
plt.plot(h3.log_Teff[nomt2[split2:]], h3.log_L[nomt2[split2:]], color='tab:orange')
plt.plot(h3.log_Teff[mt2], h3.log_L[mt2], label=r'$\mathrm{Accretor, MT}$', linestyle='dashed', color='tab:orange')

plt.xlabel(r'$\log$ $T_\mathrm{eff}$ $(\mathrm{K})$', fontsize=25)
plt.ylabel(r'$\log$ $L$ $(L_\odot)$', fontsize=25)
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


plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=25)
plt.ylabel(r'$\log_{10}$ $\dot{M}$ $(M_\odot/\mathrm{year})$', fontsize=25)
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
#Rotational speed/critical vs orbital period
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, h.surf_avg_omega_div_omega_crit, label='Donor')
plt.plot(h2.period_days, h3.surf_avg_omega_div_omega_crit, label='Accretor')
plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\omega/\omega_\mathrm{crit}$', fontsize=14)
plt.legend()
plt.savefig('wcrit.png', bbox_inches='tight')
plt.show()

#Rotational speed vs orbital period
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, h.surf_avg_omega, label='Donor')
plt.plot(h2.period_days, h3.surf_avg_omega, label='Accretor')
plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\omega$', fontsize=14)
plt.legend()
plt.savefig('omega.png', bbox_inches='tight')
plt.show()

#R_RL, R_star vs time
fig, ax1 = plt.subplots(figsize=(8, 6), dpi=100)
ax2 = ax1.twinx()
plt.rcParams["mathtext.fontset"] = 'cm'
ax1.plot(h2.period_days, np.log10(h2.rl_1), label=r'$R_{L,1}$', linestyle='dashed', color='tab:blue')
ax1.plot(h2.period_days, np.log10(h2.star_1_radius), label=r'$R_1$', color='tab:blue')
ax2.plot(h2.period_days, np.log10(h2.rl_2), label=r'$R_{L,2}$', linestyle='dashed', color='tab:orange')
ax2.plot(h2.period_days, np.log10(h2.star_2_radius), label=r'$R_2$', color='tab:orange')

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

plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=25)
plt.ylabel(r'$M/M_\odot$', fontsize=25)
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

plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\mathrm{Mass}$ $\mathrm{fraction}$', fontsize=14)
plt.savefig('conv1.png', bbox_inches='tight')
plt.show()

plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.fill_between(h2.period_days, h3.conv_mx2_bot, h3.conv_mx2_top, facecolor='tab:orange')

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
