import units_QBD as uqbd
import numpy

def p(energy__grid, ldos, F_v, T):
    de = energy__grid[1] - energy__grid[0]
    p = []
    for energies in ldos:
        p.append(0)
        for energy in energies:
            p[-1] += de * energy / (1 + numpy.exp((F_v - energy) / uqbd.K_B[0] / T)) 
    return p

def n(energy__grid, ldos, F_c, T):
    de = energy__grid[1] - energy__grid[0]
    n = []
    for energies in ldos:
        n.append(0)
        for energy in energies:
            n[-1] += de * energy / (1 + numpy.exp((energy - F_c) / uqbd.K_B[0] / T)) 
    return n