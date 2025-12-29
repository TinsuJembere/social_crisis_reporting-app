# Community Crisis Reporting & Response Platform - Backend

This is the FastAPI backend for the Community Crisis Reporting & Response Platform.

## Step 1: Backend Setup - Complete ✅

### What We've Created

1. **Project Structure**
   - `app/` - Main application directory
   - `app/__init__.py` - Package initialization
   - `app/database.py` - Database configuration and session management
   - `app/models.py` - SQLAlchemy models (User and Issue)
   - `app/main.py` - FastAPI application entry point
   - `alembic/` - Database migration scripts
   - `requirements.txt` - Python dependencies

2. **Database Models**
   - **User Model**: id, name, email, password_hash, role (user/admin), timestamps
   - **Issue Model**: id, title, description, category, status, latitude, longitude, image_url, timestamps, reporter_id

3. **Database Configuration**
   - Supports both SQLite (default) and PostgreSQL
   - Uses environment variables for configuration
   - SQLAlchemy ORM for database operations

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
copy .env.example .env  # Windows
# or
cp .env.example .env    # macOS/Linux
```

Edit `.env` and update the `SECRET_KEY` with a random string (for production).

### 5. Initialize Alembic (Database Migrations)

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. Run the Server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### 7. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing the Setup

1. Visit `http://localhost:8000` - You should see a welcome message
2. Visit `http://localhost:8000/docs` - You should see the interactive API documentation
3. Visit `http://localhost:8000/health` - You should see `{"status": "healthy"}`

## Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `name` (String, 100 chars)
- `email` (String, 100 chars, Unique)
- `password_hash` (String, 255 chars)
- `role` (Enum: user, admin)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Issues Table
- `id` (Integer, Primary Key)
- `title` (String, 200 chars)
- `description` (Text)
- `category` (Enum: infrastructure, safety, environment, health, other)
- `status` (Enum: pending, in_progress, resolved, closed)
- `latitude` (Float)
- `longitude` (Float)
- `image_url` (String, 500 chars, Nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `reporter_id` (Integer, Foreign Key to Users)

## Next Steps

In the next step, we'll implement:
- JWT-based authentication
- User registration and login endpoints
- Password hashing
- Role-based access control

## Troubleshooting

1. **Import errors**: Make sure you've activated the virtual environment
2. **Database errors**: Ensure the database URL in `.env` is correct
3. **Migration errors**: Run `alembic upgrade head` to apply migrations
4. **Port already in use**: Change the port with `--port 8001` flag

