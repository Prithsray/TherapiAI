#!/bin/bash

# Start Rasa server
rasa run  &

# Start Rasa action server
rasa run actions &

# Start Flask app with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
