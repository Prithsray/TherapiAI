@echo off

rem Start Rasa server
start rasa run 

rem Start Rasa action server
start rasa run actions --debug



rem Start UI server
python app.py

