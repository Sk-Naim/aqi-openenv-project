from openenv.core.env_server.types import Action, Observation
from pydantic import Field
from typing import Optional, Dict, Any


# ==============================
# 🔥 ACTION MODEL
# ==============================
class AQIAction(Action):
    """
    Action sent by RL agent / ESP32 controller
    """

    action: int = Field(
        ...,
        ge=0,
        le=2,
        description="Control action: 0 = idle, 1 = moderate control, 2 = aggressive control"
    )


# ==============================
# 🔥 OBSERVATION MODEL
# ==============================
class AQIObservation(Observation):
    """
    Observation returned from environment
    Includes AQI + hardware + RL metrics
    """

    # Core environment state
    aqi: float = Field(..., ge=0, le=500, description="Air Quality Index (0–500)")
    temperature: float = Field(..., description="Ambient temperature (°C)")
    noise: float = Field(..., description="Environmental noise factor")

    # Communication + hardware metrics
    pdr: float = Field(..., ge=0, le=1, description="Packet Delivery Ratio (0–1)")
    energy: float = Field(..., ge=0, description="Total energy consumed")

    # RL outputs
    reward: float = Field(..., description="Reward signal for RL agent")
    done: bool = Field(..., description="Episode termination flag")

    # Optional metadata (used in your environment step)
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional info like step count"
    )