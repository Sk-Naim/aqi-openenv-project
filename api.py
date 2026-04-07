from fastapi import FastAPI
from pydantic import BaseModel
import csv, os
from datetime import datetime
import numpy as np

app = FastAPI()

# ---------- Models ----------
class SensorData(BaseModel):
    gas: int

class Action(BaseModel):
    action: int

# ---------- STATE ----------
state = [150.0, 30.0, 0.5]

# ---------- RL Q-TABLE ----------
Q = {}

def get_state_key(aqi):
    return int(aqi // 50)

def choose_action(state):
    key = get_state_key(state[0])

    if key not in Q:
        Q[key] = [0, 0, 0]

    return int(np.argmax(Q[key]))

# ---------- METRICS ----------
total_tx = 0
success_tx = 0
energy_per_tx = 0.1584

# ---------- CSV ----------
file_name = "aqi_data.csv"

if not os.path.exists(file_name):
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time","Gas","AQI","Action","PDR","Energy"])

# ---------- SENSOR ENDPOINT ----------
@app.post("/data")
def receive_data(data: SensorData):
    global state, total_tx, success_tx

    gas = data.gas
    total_tx += 1

    # AQI conversion
    aqi = int((gas / 4095) * 500)

    # RL decision
    action = choose_action([aqi, 30, 0.5])

    success_tx += 1

    pdr = success_tx / total_tx
    total_energy = total_tx * energy_per_tx

    state[0] = aqi

    # Save CSV
    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            gas,
            aqi,
            action,
            round(pdr,3),
            round(total_energy,3)
        ])

    return {
        "action": action,
        "aqi": aqi,
        "pdr": round(pdr,3),
        "energy": round(total_energy,3)
    }

# ---------- OPENENV ----------
@app.get("/reset")
def reset():
    global state
    state = [150.0, 30.0, 0.5]
    return {"state": state}

@app.post("/step")
def step(action: Action):
    global state

    current_state = state.copy()
    aqi = state[0]

    # Apply action
    if action.action == 1:
        aqi -= 10
    elif action.action == 2:
        aqi -= 20

    energy = 0.1584
    reward = -aqi - 0.1 * energy

    done = aqi < 50

    next_state = [aqi, state[1], state[2]]

    # RL UPDATE
    key = int(current_state[0] // 50)
    next_key = int(aqi // 50)

    if key not in Q:
        Q[key] = [0,0,0]
    if next_key not in Q:
        Q[next_key] = [0,0,0]

    lr = 0.1
    gamma = 0.9

    Q[key][action.action] += lr * (
        reward + gamma * max(Q[next_key]) - Q[key][action.action]
    )

    state[0] = aqi

    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def get_state():
    return {"state": state}
