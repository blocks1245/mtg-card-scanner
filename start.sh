#!/bin/bash

if [ -d ".venv" ]; then
    echo "Found virtual environment"
else
    echo "Virtual environment not found"
    echo "Creating virtual environment, this may take a few minutes"
    python3 -m venv .venv
    echo "Installing libraries, this may take a few minutes"
    .venv/bin/pip install -r requirements.txt
fi

echo "Starting Python script"
.venv/bin/python main.py
