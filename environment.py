import numpy as np

class AQIEnvironment:
    def __init__(self):
        self.state = None

    def reset(self):
        self.state = np.array([150.0, 30.0, 0.5])
        return self.state

    def step(self, action):
        aqi = self.state[0]

        if action == 1:
            aqi -= 10
        elif action == 2:
            aqi -= 20

        energy = 0.1584
        reward = -aqi - 0.1 * energy

        done = aqi < 50

        self.state[0] = aqi
        return self.state, reward, done, {}