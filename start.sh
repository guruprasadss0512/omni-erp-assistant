#!/bin/bash
# Omni Erp Assistant — quick start script
cd ~/omni-erp-assistant
source venv/bin/activate
echo "Starting Omni Erp Assistant..."
uvicorn main:app --reload
ngrok http 8000