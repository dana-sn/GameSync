GameSync

Game catalogue synchronization using FastAPI and PostgreSQL.

About the Project

GameSync is a small integration project that demonstrates how two applications can exchange and synchronize video game catalogue data through APIs.

The project consists of two FastAPI applications connected to a PostgreSQL database, with a simple web interface for viewing and managing game entries.

Features

Two separate FastAPI applications
REST API endpoints for working with game data
Synchronization of game catalogues between applications
PostgreSQL database integration
Simple web interface
API documentation provided by Swagger UI

Technologies

Python
FastAPI
PostgreSQL
psycopg2
HTTPX
HTML

Requirements

Python 3
PostgreSQL
Git


Setup

1. Clone the repository:
git clone https://github.com/DanaSN/GameSync.git
cd GameSync

2. Install the dependencies:
py -m pip install -r requirements.txt

3. Create a .env file in the project directory and configure your environment variables:
DB_PASSWORD=your_database_password
API_KEY=your_api_key

4. Create a PostgreSQL database named gamesync and configure the database connection in database.py.


Running the Applications

Open three terminals in the project directory.

Terminal 1 — Application A
py -m uvicorn app_a:app --reload --port 8000

Terminal 2 — Application B
py -m uvicorn app_b:app --reload --port 8001

Terminal 3 — Web interface
py -m http.server 5500

Open the following addresses in your browser:
Web interface: http://127.0.0.1:5500/index.html
Application A API docs: http://127.0.0.1:8000/docs
Application B API docs: http://127.0.0.1:8001/docs

Purpose
This project was created as an educational assignment to demonstrate API integration, data exchange, and synchronization between applications.

Authors
dana-sn
ShcherbakDaria