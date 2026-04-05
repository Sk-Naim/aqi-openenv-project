import os
import requests

API_BASE = os.getenv("API_BASE_URL", "http://localhost:7860")

tasks = {
    "easy": 100,
    "medium": 70,
    "hard": 50
}

def grade(final_aqi, target):
    score = max(0.0, min(1.0, target / max(final_aqi, 1)))
    return round(score, 2)

print("[START]")

results = {}

for task, target in tasks.items():
    requests.get(f"{API_BASE}/reset")

    for step in range(10):
        state = requests.get(f"{API_BASE}/state").json()["state"]
        aqi = state[0]

        action = 2 if aqi > target else 0

        res = requests.post(f"{API_BASE}/step", json={"action": action}).json()

        print(f"[STEP] task={task} step={step} aqi={aqi} action={action} reward={res['reward']}")

        if res["done"]:
            break

    final_aqi = res["state"][0]
    score = grade(final_aqi, target)
    results[task] = score

print("[END]")
print("Scores:", results)