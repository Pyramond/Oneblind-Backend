# Oneblind-Server

Backend server for Oneblind project: https://github.com/Pyramond/OneBlind

Old backend server => https://github.com/Pyramond/OneBlind-Server (archived)


## Prerequisites
- Install Python 3.11 or above
- Install Docker

## Run with Python
- Install dependencies ```pip install -r requirements.txt```
- Go to src folder ```cd .\src\```
- Run server ```uvicorn main:app```

## Run with Docker
- Create Image ```docker build -t oneblind-server .```
- Run Image ```docker run -p 8000:8000 oneblind-server```
