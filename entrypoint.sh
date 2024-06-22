#!/bin/bash

# Start Rasa server
rasa run --cors "*" --enable-api --port 5005 --debug &

# Start Rasa action server
rasa run actions --port 5055 --debug &

# Start Flask app
python app.py
