@echo off

rem Start Rasa server
start rasa run 

rem Start Rasa action server
start rasa run actions --debug

rem Change directory to the UI folder
cd rasa-web-ui

rem Start UI server
python app.py

