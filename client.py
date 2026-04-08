"""
AQI Environment Client

Client interface to interact with AQI RL OpenEnv server.
"""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

# ✅ FIXED IMPORT (ABSOLUTE)
from aqi_openenv_project.models import AQIAction, AQIObservation


class AQIEnvClient(
    EnvClient[AQIAction, AQIObservation, State]
):
    """
    Client for AQI RL Environment
    """

    # ==============================
    # 🔁 STEP PAYLOAD
    # ==============================
    def _step_payload(self, action: AQIAction) -> Dict:
        """
        Convert AQIAction into JSON payload
        """
        return {
            "action": action.action
        }

    # ==============================
    # 📥 PARSE STEP RESULT
    # ==============================
    def _parse_result(self, payload: Dict) -> StepResult[AQIObservation]:
        """
        Convert server response → StepResult
        """

        obs_data = payload.get("observation", {})

        observation = AQIObservation(
            aqi=obs_data.get("aqi", 150.0),
            temperature=obs_data.get("temperature", 30.0),
            noise=obs_data.get("noise", 0.5),

            pdr=obs_data.get("pdr", 0.0),
            energy=obs_data.get("energy", 0.0),

            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),

            metadata=obs_data.get("metadata", {})
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

    # ==============================
    # 📊 PARSE STATE
    # ==============================
    def _parse_state(self, payload: Dict) -> State:
        """
        Convert server state → State object
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )