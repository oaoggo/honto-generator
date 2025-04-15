#!/usr/bin/env bash

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ pip list:"
pip list
