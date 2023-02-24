import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec

"""
Plots HR diagram (log L vs log T_eff) and Mdot vs orbital period (and any additional plots) for a binary model.
"""

h = mr.MesaData('LOGS1/history.data')
h2 = mr.MesaData('binary_history.data')
h3 = mr.MesaData('LOGS2/history.data')


#HR diagram with mass transfer indicated
mt =  np.where(10**(h2.lg_mstar_dot_1) > 10e-12)
mt2 =  np.where(10**(h2.lg_mstar_dot_2) > 10e-12)

plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h.log_Teff, h.log_L, label=r'$\mathrm{Donor}$', color='tab:blue')
plt.plot(h.log_Teff[mt], h.log_L[mt], label=r'$\mathrm{Donor, MT}$', color='tab:red')
plt.plot(h3.log_Teff, h3.log_L, label=r'$\mathrm{Accretor}$', color='tab:orange')
plt.plot(h3.log_Teff[mt2], h3.log_L[mt2], label=r'$\mathrm{Accretor, MT}$', color='tab:green')

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
ax[0].plot(h2.period_days, h2.lg_mstar_dot_2, label='Accretor, total mass accretion rate', color='green')
ax[0].plot(h2.period_days, h2.lg_wind_mdot_1, label='Donor, wind mass loss rate', linestyle='--', color='orange')
ax[0].plot(h2.period_days, h2.lg_wind_mdot_2, label='Accretor, wind mass loss rate', linestyle='--', color='red')
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
plt.figure(figsize=(8,6), dpi=100)
plt.rcParams["mathtext.fontset"] = 'cm'
plt.plot(h2.period_days, np.log10(h2.rl_1), label=r'$R_{L,1}$', linestyle='dashed', color='tab:red')
plt.plot(h2.period_days, np.log10(h2.star_1_radius), label=r'$R_1$', color='tab:blue')
plt.plot(h2.period_days, np.log10(h2.rl_2), label=r'$R_{L,2}$', linestyle='dashed', color='tab:green')
plt.plot(h2.period_days, np.log10(h2.star_2_radius), label=r'$R_2$', color='tab:orange')
plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$\log_{10}$ $R/R_\odot$',fontsize=14)
plt.legend()
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
plt.xlabel(r'$P_\mathrm{orb}$ $(\mathrm{days})$',fontsize=14)
plt.ylabel(r'$M/M_\odot$', fontsize=14)
plt.legend()
plt.savefig('mvsp.png', bbox_inches='tight')
plt.show()
