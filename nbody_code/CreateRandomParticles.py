import h5py
import numpy as np

############################
#NUMBER OF PARTICLES TO SIM#
############################
n = 75

# Create random data
seed = 0x4d3d3d3
np.random.seed(seed)
particle_positions = np.random.uniform(-50, 50, size=(n, 3))
particle_velocities = np.random.uniform(0, 0, size=(n, 3))
particle_masses = np.random.uniform(1000000, 100000000000, size=(n, 1))

# Write data to HDF5
try:
    data_file = h5py.File('dataset.h5', 'w')
except:
    data_file = h5py.File('dataset.h5', 'a')

data_file.create_dataset('/particle_positions', data=particle_positions)
data_file.create_dataset('/particle_velocities', data=particle_velocities)
data_file.create_dataset('/particle_masses', data=particle_masses)
data_file.create_dataset('/seed', data=seed)
data_file.close()
