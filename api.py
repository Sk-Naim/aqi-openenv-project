from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import csv
import os
from datetime import datetime

app = FastAPI()

# ---------- Typed Models ----------
class SensorData(BaseModel):
    gas: int

class Action(BaseModel):
    action: int

# ---------- State ----------
state = [150.0, 30.0, 0.5]  # [AQI, temp, noise]

# ---------- Metrics ----------
total_tx = 0
success_tx = 0
energy_per_tx = 0.1584  # Joules approx

# ---------- CSV Setup ----------
file_name = "aqi_data.csv"

if not os.path.exists(file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Gas", "AQI", "Action", "PDR", "Energy"])

# ---------- AQI Endpoint ----------
@app.post("/data")
def receive_data(data: SensorData):
    global state, total_tx, success_tx

    gas = data.gas
    total_tx += 1

    # AQI calculation
    aqi = int((gas / 4095) * 500)

    # Action logic
    if aqi > 150:
        action = 2
    elif aqi > 100:
        action = 1
    else:
        action = 0

    success_tx += 1
    pdr = success_tx / total_tx
    total_energy = total_tx * energy_per_tx

    state[0] = aqi

    # ---------- SAVE TO CSV ----------
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
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

# ---------- OpenEnv REQUIRED ----------
@app.get("/reset")
def reset():
    global state
    state = [150.0, 30.0, 0.5]
    return {"state": state}

@app.post("/step")
def step(action: Action):
    global state

    aqi = state[0]

    if action.action == 1:
        aqi -= 10
    elif action.action == 2:
        aqi -= 20

    energy = 0.1584
    reward = -aqi - 0.1 * energy

    done = aqi < 50
    state[0] = aqi

    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def get_state():
    return {"state": state}