import numpy as np
import matplotlib.pyplot as plt


def simulate_p_control():
    dt = 1.0
    t_end = 10000
    time = np.arange(0, t_end + dt, dt)

    rho = 9000.0
    cp = 176.0
    volume = 1.0e-3
    surface_area_edge = 5.0e-2
    surface_area_center = 4.0e-2
    conduction_area = 1.0e-2
    block_length = 0.1
    ambient = 25.0
    h = 14.5
    thermal_conductivity = 49.0

    mass = rho * volume
    heat_capacity = mass * cp

    k_loss_edge = h * surface_area_edge
    k_loss_center = h * surface_area_center
    k_loss = np.array([k_loss_edge, k_loss_center, k_loss_edge])

    k_cond = thermal_conductivity * conduction_area / block_length

    target_temperature = np.array([320.0, 320.0, 320.0])

    # Proportional gain [W/degC]
    Kp = np.array([8.0, 8.0, 8.0])

    heater_min = 0.0
    heater_max = 500.0

    temperature = np.zeros((len(time), 3))
    temperature[0, :] = ambient

    heater_history = np.zeros((len(time), 3))

    for i in range(len(time) - 1):
        T1, T2, T3 = temperature[i, :]

        # =====================================
        # P Control
        #
        # Heater Output
        # = Kp * Temperature Error
        # =====================================
        error = target_temperature - temperature[i, :]
        heater_output = Kp * error
        heater_output = np.clip(heater_output, heater_min, heater_max)
        heater_history[i, :] = heater_output

        # =====================================
        # Zone 1 Energy Balance
        # =====================================
        dT1 = (
            heater_output[0]
            - k_loss[0] * (T1 - ambient)
            + k_cond * (T2 - T1)
        ) / heat_capacity

        # =====================================
        # Zone 2 Energy Balance
        # =====================================
        dT2 = (
            heater_output[1]
            - k_loss[1] * (T2 - ambient)
            + k_cond * (T1 - T2)
            + k_cond * (T3 - T2)
        ) / heat_capacity

        # =====================================
        # Zone 3 Energy Balance
        # =====================================
        dT3 = (
            heater_output[2]
            - k_loss[2] * (T3 - ambient)
            + k_cond * (T2 - T3)
        ) / heat_capacity

        temperature[i + 1, 0] = T1 + dT1 * dt
        temperature[i + 1, 1] = T2 + dT2 * dt
        temperature[i + 1, 2] = T3 + dT3 * dt

    heater_history[-1, :] = heater_history[-2, :]

    return time, temperature, heater_history


def plot_p_control_result():
    time, temperature, heater_history = simulate_p_control()
    time_min = time / 60

    plt.figure(figsize=(10, 6))
    plt.plot(time_min, temperature[:, 0], label="Zone 1")
    plt.plot(time_min, temperature[:, 1], label="Zone 2")
    plt.plot(time_min, temperature[:, 2], label="Zone 3")
    plt.axhline(320, linestyle="--", label="Target temperature")

    plt.xlabel("Time [min]")
    plt.ylabel("Temperature [degC]")
    plt.title("Fig.2 Temperature Response with P Control")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("p_control_temperature_response.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_p_control_result()