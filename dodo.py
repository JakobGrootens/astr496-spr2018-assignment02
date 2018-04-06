from doit.tools import run_once
import h5py
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation
from nbody_code.ParticleClasses import *
from mpl_toolkits.mplot3d import Axes3D

def task_generate_gaussian():
    N = 32**2
    seed = 0x4d3d3d3
    fn = "gaussian.h5"
    def _generate():
        np.random.seed(seed)
        pos = np.random.normal(loc = [0.5, 0.5, 0.5], scale = 0.2, size = (N, 3))
        vel = np.random.random(size = (N, 3)) * 10.0 - 5.0
        with h5py.File(fn, "w") as f:
            f.create_dataset("/particle_positions", data = pos)
            f.create_dataset("/particle_velocities", data = vel)
            f.create_dataset("/particle_masses", data = np.ones(N))
    return {'actions': [_generate],
            'targets': [fn],
            'uptodate': [run_once]}

def task_user_simulation():

    input = "gaussian.h5"
    output = "gaussian_after.h5"

    def _simulation():
        ###################
        #NAME OF HDF5 FILE#
        ###################

        data_file = h5py.File(input, 'r')

        #########################
        #BACKGROUND FIELD AND   #
        #TOGGLE ONLY BACKGROUND #
        #########################
        x = 0
        y = 0
        z = 0
        background = [x,y,z]

        strictly_background = False

        ##########################
        #INTEGRATOR SELECTION    #
        #0 = direct euler        #
        #1 = implicit euler      #
        #2 = leapfrog            #
        ##########################

        integrator = 0

        # List all groups
        print("Keys: %s" % list(data_file.keys()))
        a_group_key = list(data_file.keys())[0]

        # Get the data
        positions = list(data_file['/particle_positions'])
        velocities = list(data_file['/particle_velocities'])
        masses = list(data_file['/particle_masses'])

        particles = []
        #Build particles from HDF5 data
        for i in range (len(positions)):
            particle = Particle(positions[i][0], positions[i][1], positions[i][2],
                                velocities[i][0], velocities[i][1], velocities[i][2],
                                masses[i])
            particles.append(particle)

        engine = Engine(background, particles, strictly_background)
        engine.euler(0, integrator)

        runtime = 1.0
        step = .5

        while (runtime > engine.t):
            engine.euler(step, integrator)

        engine.write_to_file(output)
        data_file.close()

    return {
	'actions': [_simulation],
    'targets': [output],
    'uptodate': [None]
    }
