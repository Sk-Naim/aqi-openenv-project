from fastapi import FastAPI, Body
from openenv.core.env_server.http_server import create_app

# ✅ FIXED IMPORT (IMPORTANT)
from aqi_rl_project.models import AQIAction, AQIObservation
from aqi_rl_project.server.environment import AQIEnvironment

import numpy as np
import csv, os
from datetime import datetime

# ==============================
# 🔥 OPENENV APP (MAIN APP)
# ==============================
app = create_app(
    AQIEnvironment,
    AQIAction,
    AQIObservation,
    env_name="aqi_openenv_project",
    max_concurrent_envs=2,
)

# ==============================
# 🔥 RL + SENSOR LOGIC
# ==============================
Q = {}
state = [150.0, 30.0, 0.5]

total_tx = 0
success_tx = 0
energy_per_tx = 0.1584

file_name = "aqi_data.csv"


def get_state_key(aqi):
    return int(aqi // 50)


def choose_action(aqi):
    key = get_state_key(aqi)

    if key not in Q:
        Q[key] = [0, 0, 0]

    return int(np.argmax(Q[key]))


# ==============================
# 🔥 SENSOR API (ESP32 → SERVER)
# ==============================
@app.post("/sensor")
def receive_data(gas: int = Body(...)):
    global state, total_tx, success_tx

    total_tx += 1

    # AQI conversion (hardware scaling)
    aqi = int((gas / 4095) * 500)

    # RL decision
    action = choose_action(aqi)

    success_tx += 1

    # Metrics
    pdr = success_tx / total_tx
    total_energy = total_tx * energy_per_tx

    state[0] = aqi

    # CSV logging (safe)
    if not os.path.exists(file_name):
        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time","Gas","AQI","Action","PDR","Energy"])

    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            gas,
            aqi,
            action,
            round(pdr, 3),
            round(total_energy, 3)
        ])

    return {
        "action": action,
        "aqi": aqi,
        "pdr": round(pdr, 3),
        "energy": round(total_energy, 3)
    }


# ==============================
# 🔥 HEALTH CHECK (OPTIONAL)
# ==============================
@app.get("/")
def home():
    return {"status": "AQI RL Server Running 🚀"}