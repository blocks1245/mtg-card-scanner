@echo off
if exist .venv (
    echo found virtual environment
) else (
    echo virtual environment not found
    echo creating virtual environment, this may take a few minutes
    py -m venv .venv
    echo installing libraries, this may take a few minutes
    .venv\Scripts\pip.exe install -r requirements.txt
)

echo starting python script
.venv\Scripts\python.exe main.py