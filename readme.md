# A News tracker App with PostgreSQL, Swagger & Docker

A Flask application using SQLAlchemy ORM, APScheduler for tracking news, PostgreSQL for storage, and Swagger UI for interactive API documentation.

 Everything runs in Docker via Docker Compose.

---

## Features

* **REST API** with Flask
* **Database**: PostgreSQL via SQLAlchemy ORM
* **Tasks**: Scheduled with APScheduler
* **Swagger UI**: Auto-generated API docs with Flask-Swagger or flasgger
* **Dockerized**: Production-ready deployment using Docker Compose

---

## 🗂️ Project Structure

```
├── app/
│   ├── models/
|       ├──article.py
|       └──author.py
│   ├── routes/
|       ├──article_routes.py
|       ├──author_routes.py
|       └──tracker_routes.py
│   ├── __innit__.py
│   ├── config.py
│   ├── extensions.py
│   └── tasks.py
├── db/
|   └──init.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
├── .env
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/flask-scheduler-app.git
cd flask-scheduler-app
```

### 2. Create a `.env` file

```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:password@db:5432/app_db
```

### 3. Build and Run Docker containers

```bash
docker compose up --build
```

### 4. Access the services

* API base: `http://localhost:5000/`
* Swagger UI: `http://localhost:5000/apidocs`

---

## ✅ API Usage

* `GET /` — Welcome
* `GET /tasks` — List tasks
* `POST /tasks` — Create task

---

## 📄 License

MIT
