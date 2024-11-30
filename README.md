# Student Management System

## Prerequisites
- Docker
- Docker Compose

## Setup
1. Clone repository
2. Create `.env` files:
```bash
# api/.env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=students
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## Development
```bash
# Start services
docker-compose up -d

# Apply migrations
docker-compose exec api alembic upgrade head

# Seed database
docker-compose exec api python -m app.infrastructure.database.seed

# View logs 
docker-compose logs -f
```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
.
├── api/                 # FastAPI backend
├── frontend/           # React frontend
├── docker-compose.yml
└── README.md
```