#!/bin/bash

echo "setting up Python virtual environment called venv"
python3 -m venv venv

echo "activating the virtual environment in current terminal session"
source venv/bin/activate

echo "installing all required base dependencies and modules for the project from requirements.txt"
pip install -r requirements.txt

echo "Installing large Spacy english model in virtual environment"
python3 -m spacy download en_core_web_lg

echo "Finished project setup"

