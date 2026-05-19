from particles import Particle, root_data
import matplotlib.pyplot as plt
import numpy as np

PARTICLE_NAMES = {
    "muplus": "muplus",
    "muminus": "muminus",
    "bplus": "Bplus",
    "kplus": "Kplus",
    "jpsi": "J_psi_1S",
}

root = root_data()

particles = {
    variable_name: Particle(root, particle_name).blueprint()
    for variable_name, particle_name in PARTICLE_NAMES.items()
}

muplus = particles["muplus"]
muminus = particles["muminus"]
bplus = particles["bplus"]
kplus = particles["kplus"]
jpsi = particles["jpsi"]

limit = 10000
momentum = bplus.px**2 * bplus.py**2 * bplus.pz**2

value = bplus.pt[:limit]
events = np.arange(len(value))
plt.plot(events, value)
plt.show()
print(min(value))









