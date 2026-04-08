# ==============================
# 🚀 BASE IMAGE
# ==============================
FROM python:3.12-slim

# ==============================
# 📁 WORK DIRECTORY
# ==============================
WORKDIR /app

# ==============================
# 📦 SYSTEM DEPENDENCIES
# ==============================
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# 📂 COPY PROJECT FILES
# ==============================
COPY .. /app

# ==============================
# 📦 INSTALL PYTHON DEPENDENCIES
# ==============================
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/server/requirements.txt

# ==============================
# 🔧 ENV VARIABLES
# ==============================
ENV PYTHONPATH="/app"

# ==============================
# ❤️ HEALTH CHECK
# ==============================
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD curl -f http://localhost:8000/ || exit 1

# ==============================
# 🚀 START SERVER
# ==============================
CMD ["uvicorn", "aqi_openenv_project.server.app:app", "--host", "0.0.0.0", "--port", "8000"]