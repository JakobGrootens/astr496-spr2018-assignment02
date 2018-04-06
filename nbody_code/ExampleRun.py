import h5py
import matplotlib
import matplotlib.animation
import matplotlib.pyplot as plt
from ParticleClasses import *
from mpl_toolkits.mplot3d import Axes3D

###################
#NAME OF HDF5 FILE#
###################
filename = input("Input the file name... \n")
data_file = h5py.File(filename, 'r')

#########################
#BACKGROUND FIELD AND   #
#TOGGLE ONLY BACKGROUND #
#########################
x = input("Input x field value...  ")
y = input("Input y field value...  ")
z = input("Input z field value...  ")
background = [int(x),int(y),int(z)]

print("\nWould you like to include inter-force interactions?")
user_input = input("Type y for yes and n for no...\n")
if user_input == "y":
    strictly_background = False
elif user_input == "n":
    strictly_background = True

##########################
#INTEGRATOR SELECTION    #
#0 = direct euler        #
#1 = implicit euler      #
#2 = leapfrog            #
##########################
integrator = input("\nWhat integrator would you like to use?\n0 = direct euler\n1 = implicit euler\n2 = leapfrog\n")
integrator = int(integrator)

# Code to list all groups (for debugging)
#print("Keys: %s" % list(data_file.keys()))
#a_group_key = list(data_file.keys())[0]

# Get the data
positions = list(data_file['/particle_positions'])
velocities = list(data_file['/particle_velocities'])
masses = list(data_file['/particle_masses'])

print("\nWould you like to output plots?")
user_input = input("Type y for yes and n for no...\n")
if user_input == "y":
    plot_enabled = True
elif user_input == "n":
    plot_enabled = False

print("Please wait while the file is loaded...")

particles = []
#Build particles from HDF5 data
for i in range (len(positions)):
    particle = Particle(positions[i][0], positions[i][1], positions[i][2],
                        velocities[i][0], velocities[i][1], velocities[i][2],
                        masses[i])
    particles.append(particle)

engine = Engine(background, particles, strictly_background)

engine.euler(0, integrator)
engine.plot_positions()

runtime = int(input("\nHow long would you like your simulation to last?"))
step = 1


flag = 0
while (runtime > engine.t):

    if (engine.t > (runtime * .75)):
        if flag == 2:
            print("75% done...")
            flag = 1
    elif (engine.t > (runtime / 2) and flag == 1):
        print("50% done...")
        flag = 2
    elif (engine.t > (runtime/ 4) and flag == 0):
        print("25% done...")
        flag = 1

    engine.euler(step, integrator)
    if plot_enabled:
        engine.plot_positions()

print("Simulation complete!")

filename = filename[:-3]
filename = filename + "_updated.h5"
print("Updated positions written to " + filename)
engine.write_to_file(filename)

data_file.close()
