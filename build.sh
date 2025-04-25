#!/bin/bash

echo "[1/4] Activating virtual environment..."
source chatenv/bin/activate || { echo "Missing venv? Try: python3 -m venv chatenv"; exit 1; }

echo "[2/4] Installing dependencies..."
pip install -r requirements.txt

echo "[3/4] Building APK..."
buildozer -v android debug

echo "[4/4] Done. Find your APK in: bin/"
