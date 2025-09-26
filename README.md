# Oneblind-Server

Backend server for Oneblind project: https://github.com/Pyramond/OneBlind


## Prerequisites
- Install Python 3.11 or above
- Install Docker

## Configuration

### Use Supabase PostGreSQL Database

- Create supabase project and copy both connection link and project's password
- Create .env file at the project's root and set the connection link

.env exemple
```
DB_URL='postgresql://postgres:[PASSWORD]@db.[ID].supabase.co:5432/postgres'
```

### Use SQLite

- Create .env file at project's root
.env
```
DB_URL='sqlite:///./static/database.db'
```

- Modify src/db/database.py
```python

# Before
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# After
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
```

## Run with Python
- Install dependencies ```pip install -r requirements.txt```
- Go to src folder ```cd .\src\```
- Run server ```uvicorn main:app```

## Run with Docker
- Create Image ```docker build -t oneblind-server .```
- Run Image ```docker run -p 8000:8000 oneblind-server```
