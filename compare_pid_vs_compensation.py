import matplotlib.pyplot as plt

from pid_disturbance_simulation import simulate_pid_control as simulate_pid_only
from pid_with_compensation_simulation import simulate_pid_control as simulate_pid_compensation


def plot_temperature_comparison():
    # =====================================
    # Run simulations
    # =====================================
    time_pid, temperature_pid, _ = simulate_pid_only()
    time_comp, temperature_comp, _ = simulate_pid_compensation()

    time_min_pid = time_pid / 60
    time_min_comp = time_comp / 60

    # =====================================
    # Plot temperature comparison
    # =====================================
    plt.figure(figsize=(10, 6))

    plt.plot(time_min_pid, temperature_pid[:, 1], label="Zone 2: PID only")
    plt.plot(time_min_comp, temperature_comp[:, 1], label="Zone 2: PID + compensation")

    plt.plot(time_min_pid, temperature_pid[:, 0], linestyle="--", label="Zone 1: PID only")
    plt.plot(time_min_comp, temperature_comp[:, 0], linestyle="--", label="Zone 1: PID + compensation")

    plt.axhline(320, linestyle=":", label="Target temperature")

    plt.xlabel("Time [min]")
    plt.ylabel("Temperature [degC]")

    plt.xlim(145, 175)
    plt.ylim(280, 350)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/fig11_temperature_response_comparison_zoom.png", dpi=300)
    plt.show()


def plot_heater_output_comparison():
    # =====================================
    # Run simulations
    # =====================================
    time_pid, _, heater_pid = simulate_pid_only()
    time_comp, _, heater_comp = simulate_pid_compensation()

    time_min_pid = time_pid / 60
    time_min_comp = time_comp / 60

    # =====================================
    # Plot heater output comparison
    # =====================================
    plt.figure(figsize=(10, 6))

    plt.plot(time_min_pid, heater_pid[:, 1], label="Zone 2 heater: PID only")
    plt.plot(time_min_comp, heater_comp[:, 1], label="Zone 2 heater: PID + compensation")

    plt.plot(time_min_pid, heater_pid[:, 0], linestyle="--", label="Zone 1 heater: PID only")
    plt.plot(time_min_comp, heater_comp[:, 0], linestyle="--", label="Zone 1 heater: PID + compensation")

    plt.xlabel("Time [min]")
    plt.ylabel("Heater output [W]")

    plt.xlim(145, 175)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/fig12_heater_output_comparison_zoom.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_temperature_comparison()
    plot_heater_output_comparison()