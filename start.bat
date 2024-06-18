@echo off

rem Start Rasa server
start rasa run --cors "*" --enable-api --debug

rem Start Rasa action server
start rasa run actions

rem Change directory to the UI folder
cd rasa-web-ui

rem Start UI server
python app.py

