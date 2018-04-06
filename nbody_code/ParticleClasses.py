#Particle class from lecture with z-component addedzz
import matplotlib
import matplotlib.animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import h5py
import math

class Particle:
    def __init__(self, x, y, z, vx, vy, vz, mass):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass

    def implicit_update(self, Fx, Fy, Fz, dt):
        self.vx = self.vx + Fx / self.mass * dt
        self.vy = self.vy + Fy / self.mass * dt
        self.vz = self.vz + Fz / self.mass * dt
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        self.z = self.z + self.vz * dt

    def euler_update(self, Fx, Fy, Fz, dt):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        self.z = self.z + self.vz * dt
        self.vx = self.vx + Fx / self.mass * dt
        self.vy = self.vy + Fy / self.mass * dt
        self.vz = self.vz + Fz / self.mass * dt

    def leapfrog_update_pos(self, dt):
        self.x = self.x + self.vx * .5 * dt
        self.y = self.y + self.vy * .5 * dt
        self.z = self.z + self.vz * .5 * dt

    def leapfrog_update_velocity(self, Fx, Fy, Fz, dt):
        self.vx = self.vx + Fx / self.mass * dt
        self.vy = self.vy + Fy / self.mass * dt
        self.vz = self.vz + Fz / self.mass * dt

    def pairwise_force(self, particle):
        G = 6.674 * (10**-11)
        r2 = (self.x - particle.x)**2.0 +              (self.y - particle.y)**2.0 +              (self.z - particle.z)**2.0
        F_mag = -(G * particle.mass * self.mass * r2**.5)/(r2+100)**1.5
        F_x = (self.x - particle.x)/r2**0.5 * F_mag
        F_y = (self.y - particle.y)/r2**0.5 * F_mag
        F_z = (self.z - particle.z)/r2**0.5 * F_mag
        return (F_x, F_y, F_z)
    def distance(self, particle):
        return((self.x-particle.x)**2 + (self.y-particle.y)**2 + (self.z-particle.z)**2)**.5
    def print_particle(self):
        print("Position:", self.x, ",", self.y, ",", self.z)
        print("Velocity:", self.vx, ",", self.vy, ",", self.vz)


# In[3]:


class Engine:
    def __init__(self, background, particles, strictly_background):
        self.background = background
        self.particles = particles
        self.strictly_background = strictly_background;
        self.t = 0.0
        self.iteration = 0
    def print_positions(self):
        for particle in self.particles:
            particle.print_particle()

    def write_to_file(self, filename):
        particle_positions = []
        particle_velocities = []
        particle_masses = []
        for particle in self.particles:
           particle_positions.append((particle.x, particle.y, particle.z))
           particle_velocities.append((particle.vx, particle.vy, particle.vz))
           particle_masses.append(particle.mass)
        with h5py.File(filename, "w") as data_file:
           data_file.create_dataset('/particle_positions', data = particle_positions)
           data_file.create_dataset('/particle_velocities', data = particle_velocities)
           data_file.create_dataset('/particle_masses', data = particle_masses)

    def plot_positions(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax = fig.gca(projection='3d')
        square = 200
        ax.set_xlim(-1*square, square)
        ax.set_ylim(-1*square, square)
        ax.set_zlim(-1*square, square)
        xs = []
        ys = []
        zs = []
        for particle in self.particles:
            xs.append(particle.x)
            ys.append(particle.y)
            zs.append(particle.z)
        ax.scatter(xs,ys,zs)
        name = 'fig'+str(self.iteration)+'.png'
        fig.savefig(name)
        plt.close(fig)
        self.iteration += 1

    def euler(self, timestep, integrator):
        self.t += timestep
        for particle in self.particles:
            if integrator == 2:
                particle.leapfrog_update_pos(timestep)

            F_x_total = self.background[0]
            F_y_total = self.background[1]
            F_z_total = self.background[2]
            if not self.strictly_background:
                for other in self.particles:
                    if other is particle:
                            continue
                    F_x, F_y, F_z = particle.pairwise_force(other)

                    F_x_total += F_x
                    F_y_total += F_y
                    F_z_total += F_z

            if integrator == 0:
                particle.euler_update(F_x_total, F_y_total, F_z_total, timestep)
            elif integrator == 1:
                particle.implicit_update(F_x_total, F_y_total, F_z_total, timestep)
            elif integrator == 2:
                particle.leapfrog_update_velocity(F_x_total, F_y_total, F_z_total, timestep)
                particle.leapfrog_update_pos(timestep)
