# AQI OpenEnv Project

## Overview
This project integrates IoT (ESP32 + MQ135 sensor) with an OpenEnv-based RL system to monitor and optimize air quality.

## Features
- Real-time AQI monitoring
- FastAPI backend
- OpenEnv environment (reset, step, state)
- RL-based decision system
- Hardware metrics (PDR, energy)

## Endpoints
- /data → receive sensor data
- /reset → reset environment
- /step → perform action
- /state → get current state

## Run
uvicorn api:app --host 0.0.0.0 --port 8000

## Deployment
Deployed using Docker on Hugging Face Spaces.
