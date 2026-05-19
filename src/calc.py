from particles import Particle, root_data
import numpy as np
import matplotlib.pyplot as plt

root = root_data()

muplus = Particle(root, 'muplus').blueprint()
muminus = Particle(root, 'muminus').blueprint()
bplus = Particle(root, 'Bplus').blueprint()
kplus = Particle(root, 'Kplus').blueprint()
jpsi = Particle(root, 'J_psi_1S').blueprint()

bp_x = np.array(bplus.momentum[0])
bp_y = np.array(bplus.momentum[1])
bp_z = np.array(bplus.momentum[2])
bp_endx = np.array(bplus.end[0])
bp_endy = np.array(bplus.end[1])
bp_endz = np.array(bplus.end[2])

mu_x = np.array(muplus.momentum[0])
mu_y = np.array(muplus.momentum[1])
mu_z = np.array(muplus.momentum[2])

mum_x = np.array(muminus.momentum[0])
mum_y = np.array(muminus.momentum[1])
mum_z = np.array(muminus.momentum[2])

bp = np.array(bplus.start)
bp_start = (bp[0], bp[1], bp[2])

x = np.divide(bp_x, bp_endx, out=np.zeros_like(bp_x, dtype=float), where=bp_endx != 0)
y = np.divide(bp_y, bp_endy, out=np.zeros_like(bp_y, dtype=float), where=bp_endy != 0)
z = np.divide(bp_z, bp_endz, out=np.zeros_like(bp_z, dtype=float), where=bp_endz != 0)
n = 100000

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

'''ax.scatter(bp_x[:n], bp_y[:n], bp_z[:n],s=1)
plt.show()'''

'''ax.scatter(mu_x[:n], mu_y[:n], mu_z[:n],s=1)
plt.show()'''

x = x**3 * y
y = y**3 * z
z = z**3 * x

ax.set_xlim(-5,9)
ax.set_ylim(-4,2)
ax.set_zlim(-6,2)

a = (max(x[:n]), min(x[:n]))
b = (max(y[:n]), max(y[:n]))
c= (max(z[:n]), max(z[:n]))
d

print(f'{a}\n'
      f'{b}\n'
      f'{c}')


print(d)


