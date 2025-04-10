#!/usr/bin/env bash
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# 설치 확인
if ! pip show flask; then
  echo "❌ Flask not found after installation"
  exit 1
fi
