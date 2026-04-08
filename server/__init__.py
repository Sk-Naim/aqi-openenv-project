"""
AQI OpenEnv Project - Server Package

This module exposes the AQIEnvironment class for use with OpenEnv
and external integrations (FastAPI, Uvicorn, Docker, etc.).
"""

from aqi_openenv_project.server.environment import AQIEnvironment

__all__ = ["AQIEnvironment"]