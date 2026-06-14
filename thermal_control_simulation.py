import numpy as np
import matplotlib.pyplot as plt

# simulation time
dt = 0.1
t_end = 100
time = np.arange(0, t_end, dt)

# temperatures
T1 = np.zeros(len(time))
T2 = np.zeros(len(time))
T3 = np.zeros(len(time))

# initial temperature
T1[0] = 25
T2[0] = 25
T3[0] = 25

# target temperature
target = 80

# PID gains
Kp = 2.0
Ki = 0.05

integral1 = 0
integral2 = 0
integral3 = 0

# heat transfer coefficient
k = 0.05

for i in range(len(time)-1):

    e1 = target - T1[i]
    e2 = target - T2[i]
    e3 = target - T3[i]

    integral1 += e1 * dt
    integral2 += e2 * dt
    integral3 += e3 * dt

    u1 = Kp * e1 + Ki * integral1
    u2 = Kp * e2 + Ki * integral2
    u3 = Kp * e3 + Ki * integral3

    dT1 = u1 + k*(T2[i]-T1[i])
    dT2 = u2 + k*(T1[i]-T2[i]) + k*(T3[i]-T2[i])
    dT3 = u3 + k*(T2[i]-T3[i])

    T1[i+1] = T1[i] + dT1*dt
    T2[i+1] = T2[i] + dT2*dt
    T3[i+1] = T3[i] + dT3*dt

plt.plot(time, T1, label="Zone1")
plt.plot(time, T2, label="Zone2")
plt.plot(time, T3, label="Zone3")

plt.axhline(target, linestyle="--", label="Target")

plt.xlabel("Time")
plt.ylabel("Temperature")
plt.legend()
plt.grid()

plt.show()
