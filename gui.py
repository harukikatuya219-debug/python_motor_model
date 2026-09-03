import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import tkinter as tk
from tkinter import ttk

from motor.motor_param import (
    MotorParam,
    # DCMotorParameter,
    # BLDCParameter,
    # PMSMParameter
)


class ParameterGUI:

    DEFAULT_MOTOR_VALUES = {
        "R": 0.5,
        "L": 0.003,
        "Ke": 0.08,
        "J": 0.01,
        "D": 0.005,
        "p": 4,
        "Kt": 0.08,
    }

    DEFAULT_SIMULATION_VALUES = {
        "sim_time": 2.0,
        "dt": 0.001,
    }

    MOTOR_CONFIG = {
        "DC": {
            "class": MotorParam,
            "fields": ["R", "L", "Ke", "J", "D", "p", "Kt"]
        },
        # "BLDC": {
        #     "class": BLDCParameter,
        #     "fields": ["R", "L", "Ke", "J", "D", "pole"]
        # },
        # "PMSM": {
        #     "class": PMSMParameter,
        #     "fields": ["R", "Ld", "Lq", "Ke", "J", "D", "pole", "Kt"]
        # }
    }

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Motor Parameter")

        self.parameter = None
        self.sim_time = (0.0, self.DEFAULT_SIMULATION_VALUES["sim_time"])
        self.dt = self.DEFAULT_SIMULATION_VALUES["dt"]

        # モータ種類
        self.motor_type = tk.StringVar(value="DC")

        ttk.Label(self.root, text="Motor Type").grid(row=0, column=0, padx=5, pady=5)

        self.combo = ttk.Combobox(
            self.root,
            textvariable=self.motor_type,
            values=list(self.MOTOR_CONFIG.keys()),
            state="readonly"
        )

        self.combo.grid(row=0, column=1, padx=5, pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.update_fields)

        # パラメータ入力欄
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=1, column=0, columnspan=2)

        self.entries = {}

        # OKボタン
        self.ok_button = ttk.Button(
            self.root,
            text="OK",
            command=self.submit
        )

        self.ok_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.update_fields()

    def update_fields(self, event=None):

        # 古いWidgetを削除
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.entries.clear()

        fields = self.MOTOR_CONFIG[self.motor_type.get()]["fields"]

        for i, name in enumerate(fields):
            ttk.Label(self.frame, text=name).grid(
                row=i,
                column=0,
                padx=5,
                pady=3,
                sticky="w"
            )

            entry = ttk.Entry(self.frame, width=15)
            entry.insert(0, str(self.DEFAULT_MOTOR_VALUES.get(name, "")))
            entry.grid(row=i, column=1)

            self.entries[name] = entry

        sim_fields = ["sim_time", "dt"]
        start_row = len(fields)

        for j, name in enumerate(sim_fields):
            ttk.Label(self.frame, text=name).grid(
                row=start_row + j,
                column=0,
                padx=5,
                pady=3,
                sticky="w"
            )

            entry = ttk.Entry(self.frame, width=15)
            entry.insert(0, str(self.DEFAULT_SIMULATION_VALUES[name]))
            entry.grid(row=start_row + j, column=1)

            self.entries[name] = entry

    def submit(self):

        values = {}

        for name, entry in self.entries.items():
            text = entry.get().strip()

            if name == "p":
                values[name] = int(float(text))
            else:
                values[name] = float(text)

        cls = self.MOTOR_CONFIG[self.motor_type.get()]["class"]
        motor_values = {name: values[name] for name in cls.__annotations__}

        self.parameter = cls(**motor_values)
        self.sim_time = (0.0, float(values["sim_time"]))
        self.dt = float(values["dt"])

        if self.dt <= 0:
            raise ValueError("dt は 0 より大きい値を入力してください")

        if self.sim_time[1] <= 0:
            raise ValueError("シミュレーション時間は 0 より大きい値を入力してください")

        self.root.destroy()

    def run(self):

        self.root.mainloop()

        return self.parameter, self.sim_time, self.dt