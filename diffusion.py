"""
An opposed-flow ethane/air diffusion flame
"""

import cantera as ct
import matplotlib.pyplot as plt
import os

# Create directory for output data files
data_directory = 'diffusion_flame_data/'
if not os.path.exists(data_directory):
    os.makedirs(data_directory)


# INPUT PARAMETERS
p = 25e3  # pressure
tin_f = 300.0  # fuel inlet temperature
tin_o = 300.0  # oxidizer inlet temperature
mdot_o = 0.944  # kg/m^2/s
mdot_f = 0.056  # kg/m^2/s
comp_o = 'O2:0.21, N2:0.78, AR:0.01'  # air
comp_f = 'C2H6:1'  # fuel

# Distance between inlets is 3 cm
width = 0.03

# Amount of diagnostic output (0 to 5)
loglevel = 1

# Create the gas object used to evaluate all thermodynamic, kinetic, and
# transport properties.
gas = ct.Solution('gri30.xml', 'gri30_mix')
gas.TP = gas.T, p

# Create an object representing the counterflow flame configuration,
# which consists of a fuel inlet on the left, the flow in the middle,
# and the oxidizer inlet on the right.


#Temperature of flame as function of pressure
f = ct.CounterflowDiffusionFlame(gas, width=width)

# Set the state of the two inlets
f.fuel_inlet.mdot = mdot_f
f.fuel_inlet.X = comp_f
f.fuel_inlet.T = tin_f

f.oxidizer_inlet.mdot = mdot_o
f.oxidizer_inlet.X = comp_o
f.oxidizer_inlet.T = tin_o

# Set the boundary emissivities
f.set_boundary_emissivities(0.0, 0.0)
f.set_refine_criteria(ratio=4, slope=0.2, curve=0.3, prune=0.04)

# Solve the problem
f.solve(loglevel, auto=True)
f.show_solution()
f.save(data_directory + 'c2h6_diffusion_pressure.xml')

# write the velocity, temperature, and mole fractions to a CSV file
f.write_csv(data_directory + 'c2h6_diffusion_pressure.csv', quiet=False)

f.show_stats(0)

# Plot temperature of flame as function of pressure
figTemperatureModifiedFlame = plt.figure()
plt.plot(f.flame.grid, f.T, label=p/100000)
plt.title('Flame temperature at distance from burner and ambient pressure [bar]')
plt.ylim(0,2500)
plt.xlim(0.000, 0.030)

# pressure loop
while p <= 125e3:
    p=p+25e3
    gas.TP = gas.T, p
    f = ct.CounterflowDiffusionFlame(gas, width=width)
    f.fuel_inlet.mdot = mdot_f
    f.fuel_inlet.X = comp_f
    f.fuel_inlet.T = tin_f
    f.oxidizer_inlet.mdot = mdot_o
    f.oxidizer_inlet.X = comp_o
    f.oxidizer_inlet.T = tin_o
    f.set_boundary_emissivities(0.0, 0.0)
    f.set_refine_criteria(ratio=4, slope=0.2, curve=0.3, prune=0.04)
    f.solve(loglevel, auto=True)
    f.show_solution()
    plt.plot(f.flame.grid, f.T, label=p/100000)
    plt.legend()
    plt.legend(loc=1)
plt.savefig(data_directory + 'c2h6_diffusion_pressure.png')



# Temperature of flame as function of air temperature
f = ct.CounterflowDiffusionFlame(gas, width=width)

# Set the state of the two inlets
f.fuel_inlet.mdot = mdot_f
f.fuel_inlet.X = comp_f
f.fuel_inlet.T = tin_f
f.oxidizer_inlet.mdot = mdot_o
f.oxidizer_inlet.X = comp_o
f.oxidizer_inlet.T = tin_o
p=1e5

# Set the boundary emissivities
f.set_boundary_emissivities(0.0, 0.0)
f.set_refine_criteria(ratio=4, slope=0.2, curve=0.3, prune=0.04)

# Solve the problem
f.solve(loglevel, auto=True)
f.show_solution()
f.save(data_directory + 'c2h6_diffusion_temperature.xml')

# write the velocity, temperature, and mole fractions to a CSV file
f.write_csv(data_directory + 'c2h6_diffusion_temperature.csv', quiet=False)
f.show_stats(0)

# Plot temperature of flame as function of air temperature
figTemperatureModifiedFlame = plt.figure()
plt.plot(f.flame.grid, f.T, label=tin_o )
plt.title('Flame temperature at distance from burner air temperatures [K]')
plt.ylim(0,2500)
plt.xlim(0.000, 0.030)

# Temperature loop
while tin_o <= 700:
    tin_o=tin_o+100
    f.fuel_inlet.T = tin_f
    f.oxidizer_inlet.T = tin_o
    f.solve(loglevel=1, refine_grid=False)
    f.show_solution()
    plt.plot(f.flame.grid, f.T, label=tin_o)
    plt.legend()
    plt.legend(loc=1)
plt.savefig(data_directory + 'c2h6_diffusion_temperature.png')
