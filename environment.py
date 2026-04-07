import numpy as np
import random

class AQIEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        # State: [AQI, temperature, noise]
        self.state = np.array([150.0, 30.0, 0.5])
        return self.state

    def step(self, action):
        aqi, temp, noise = self.state

        # Action effects
        if action == 1:
            aqi -= 8
        elif action == 2:
            aqi -= 18

        # Natural fluctuation
        aqi += random.uniform(0, 5)

        aqi = max(0, min(500, aqi))

        energy = 0.1584

        # RL reward
        reward = -aqi - 0.1 * energy

        done = aqi < 50

        self.state = np.array([aqi, temp, noise])

        return self.state, reward, done, {}
