import random
from uuid import uuid4
import numpy as np

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

# ✅ FIXED ABSOLUTE IMPORT (PERMANENT SOLUTION)
from aqi_openenv_project.models import AQIAction, AQIObservation


class AQIEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.reset()

        # RL Q-table
        self.Q = {}

        # Metrics
        self.total_tx = 0
        self.success_tx = 0
        self.energy_per_tx = 0.1584

    def reset(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.aqi = 150.0
        self.temp = 30.0
        self.noise = 0.5

        return AQIObservation(
            aqi=self.aqi,
            temperature=self.temp,
            noise=self.noise,
            pdr=0.0,
            energy=0.0,
            reward=0.0,
            done=False
        )

    def get_key(self, aqi):
        return int(aqi // 50)

    def step(self, action: AQIAction):

        self._state.step_count += 1

        current_aqi = self.aqi

        # ACTION EFFECT (hardware control simulation)
        if action.action == 1:
            self.aqi -= 8
        elif action.action == 2:
            self.aqi -= 18

        # ENVIRONMENT NOISE
        self.aqi += random.uniform(0, 5)
        self.aqi = max(0, min(500, self.aqi))

        # COMMUNICATION METRICS
        self.total_tx += 1
        self.success_tx += 1

        pdr = self.success_tx / self.total_tx
        total_energy = self.total_tx * self.energy_per_tx

        # REWARD FUNCTION (balanced for RL + hardware)
        reward = -self.aqi - 0.1 * total_energy

        done = self.aqi < 50

        # -------- RL UPDATE --------
        key = self.get_key(current_aqi)
        next_key = self.get_key(self.aqi)

        if key not in self.Q:
            self.Q[key] = [0, 0, 0]
        if next_key not in self.Q:
            self.Q[next_key] = [0, 0, 0]

        lr = 0.1
        gamma = 0.9

        self.Q[key][action.action] += lr * (
            reward + gamma * max(self.Q[next_key]) - self.Q[key][action.action]
        )

        return AQIObservation(
            aqi=self.aqi,
            temperature=self.temp,
            noise=self.noise,
            pdr=round(pdr, 3),
            energy=round(total_energy, 3),
            reward=reward,
            done=done,
            metadata={"step": self._state.step_count}
        )

    @property
    def state(self):
        return self._state
