#!/bin/bash

# Start Rasa server
rasa run --cors "*" --enable-api --debug &

# Start Rasa action server
rasa run actions --debug &

# Start Flask app
python app.py
