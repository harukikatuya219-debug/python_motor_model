import matplotlib.pyplot as plt
# def plot_result(sol):
#     fig, axes = plt.subplots(2, 1, figsize=(10, 8))
#     time = sol.t
#     current = sol.y[0]  # 状態変数1
#     speed = sol.y[1]  # 状態変数2
#     axes[0].plot(time, current)
#     axes[0].set_title("Current vs Time")
#     axes[0].set_xlabel("Time (s)")
#     axes[0].set_ylabel("Current (A)")
#     axes[0].grid()
#     axes[1].plot(time, speed)
#     axes[1].set_title("Speed vs Time")
#     axes[1].set_xlabel("Time (s)")
#     axes[1].set_ylabel("Speed (rad/s)")
#     axes[1].grid()
#     plt.tight_layout()
#     plt.show() 

def plot_result(sol_Euler, sol_RK4):
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # 時間
    time = sol_Euler.t

    # 電流
    axes[0].plot(
        time,
        sol_Euler.y[0],
        "-o",
        label="Euler",
        markersize=3,
        markevery=100
    )
    axes[0].plot(
        time,
        sol_RK4.y[0],
        "--s",
        label="RK4",
        markersize=3,
        markevery=100
    )
    axes[0].set_title("Current vs Time")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Current (A)")
    axes[0].grid(True)
    axes[0].legend()

    # 回転速度
    axes[1].plot(
        time,
        sol_Euler.y[1],
        "-o",
        label="Euler",
        markersize=3,
        markevery=100
    )
    axes[1].plot(
        time,
        sol_RK4.y[1],
        "--s",
        label="RK4",
        markersize=3,
        markevery=100
    )
    axes[1].set_title("Speed vs Time")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Speed (rad/s)")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()