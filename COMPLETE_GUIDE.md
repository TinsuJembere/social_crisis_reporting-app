# Community Crisis Reporting & Response Platform - Complete Guide

## 🎉 Project Complete!

This is a full-stack web application for reporting and managing community issues.

## 📁 Project Structure

```
crisis-reporting-platform/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── routers/      # API routes
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   └── main.py       # FastAPI app
│   └── requirements.txt
└── frontend/            # Next.js frontend
    ├── pages/           # Next.js pages
    ├── components/      # React components
    ├── utils/           # Utilities
    └── styles/          # CSS/Tailwind
```

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy env.example .env  # Windows
cp env.example .env    # macOS/Linux

# Edit .env and set SECRET_KEY

# Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Run server
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API Docs at: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

## 🔑 Features

### Backend
- ✅ JWT Authentication
- ✅ User Registration/Login
- ✅ Issue CRUD Operations
- ✅ Image Upload
- ✅ Notifications
- ✅ Role-based Access Control
- ✅ RESTful API

### Frontend
- ✅ Landing Page
- ✅ Authentication (Login/Register)
- ✅ User Dashboard
- ✅ Issue Reporting
- ✅ Issue Listing
- ✅ Issue Details
- ✅ Map View
- ✅ Responsive Design

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login/json` - Login
- `GET /api/auth/me` - Get current user

### Issues
- `GET /api/issues/` - List issues
- `GET /api/issues/{id}` - Get issue
- `POST /api/issues/` - Create issue
- `PATCH /api/issues/{id}` - Update issue
- `PUT /api/issues/{id}/status` - Update status (admin)
- `DELETE /api/issues/{id}` - Delete issue (admin)

### Notifications
- `GET /api/notifications/` - List notifications
- `GET /api/notifications/unread/count` - Unread count
- `PUT /api/notifications/{id}/read` - Mark as read
- `PUT /api/notifications/read-all` - Mark all as read

## 🔐 Default Roles

- **USER**: Can create and view issues
- **ADMIN**: Can manage all issues, update status, delete

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- JWT (python-jose)
- Bcrypt (passlib)
- Pillow (image processing)

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Axios
- Leaflet (maps)
- React Hot Toast

## 📦 Next Steps (Enhancements)

1. **Docker Setup**: Dockerize both frontend and backend
2. **Email Notifications**: Add email notifications for status changes
3. **Search**: Implement search functionality
4. **User Profile**: Add user profile page
5. **Dark Mode**: Add dark mode toggle
6. **Admin Dashboard**: Enhanced admin features
7. **Comments**: Add comments on issues
8. **File Uploads**: Support multiple images

## 🐛 Troubleshooting

1. **Port already in use**: Change port in `.env` or use different port
2. **Database errors**: Run migrations with `alembic upgrade head`
3. **CORS errors**: Check CORS settings in `backend/app/main.py`
4. **Image upload fails**: Check `UPLOAD_DIR` exists and is writable

## 📚 Documentation

- Backend API: `http://localhost:8000/docs`
- Frontend: See `frontend/README.md`
- Backend: See `backend/README.md`

## 🎯 Deployment

### Backend (Render/Fly.io)
1. Set environment variables
2. Set `DATABASE_URL` to PostgreSQL
3. Run migrations on deploy
4. Set `SECRET_KEY` securely

### Frontend (Vercel)
1. Connect GitHub repo
2. Set `NEXT_PUBLIC_API_URL` to backend URL
3. Deploy

---

**Happy Coding! 🚀**

