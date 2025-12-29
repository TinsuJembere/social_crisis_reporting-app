# Step 2: Authentication - Complete ✅

## What We've Built

### 🔐 Authentication System

1. **JWT Token Management**
   - Token creation with expiration
   - Token decoding and validation
   - Secure secret key from environment variables

2. **Password Security**
   - Bcrypt password hashing
   - Password verification
   - Secure storage of password hashes

3. **Authentication Endpoints**
   - `POST /api/auth/register` - User registration
   - `POST /api/auth/login` - Login with form data (OAuth2 standard)
   - `POST /api/auth/login/json` - Login with JSON body
   - `GET /api/auth/me` - Get current user info (protected)

4. **Dependency Injection System**
   - `get_current_user` - Get authenticated user from JWT
   - `get_current_active_user` - Get active user (for future account status)
   - `get_current_admin_user` - Admin-only access control

### 📁 Files Created/Modified

1. ✅ `backend/app/utils.py` - Authentication utilities (JWT, password hashing, dependencies)
2. ✅ `backend/app/routers/__init__.py` - Router package initialization
3. ✅ `backend/app/routers/auth.py` - Authentication endpoints
4. ✅ `backend/app/schemas.py` - Added auth schemas (Token, UserLogin, UserRegister)
5. ✅ `backend/app/main.py` - Added auth router

## 🔑 Key Features

### Password Hashing
- Uses bcrypt via passlib
- Secure one-way hashing
- Password verification on login

### JWT Tokens
- Contains user ID, email, and role
- Configurable expiration time (default: 30 minutes)
- Secure signing with secret key

### Role-Based Access Control
- User roles: `USER` and `ADMIN`
- Admin-only endpoints using `get_current_admin_user`
- Ready for protected routes in next steps

## 📡 API Endpoints

### 1. Register New User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2024-01-01T12:00:00"
}
```

### 2. Login (OAuth2 Form Data)
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=john@example.com&password=securepassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Login (JSON)
```http
POST /api/auth/login/json
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. Get Current User (Protected)
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2024-01-01T12:00:00"
}
```

## 🧪 Testing the Authentication

### Using Swagger UI (Recommended)

1. Start the server:
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn app.main:app --reload
   ```

2. Visit `http://localhost:8000/docs`

3. **Test Registration:**
   - Find `POST /api/auth/register`
   - Click "Try it out"
   - Enter user data:
     ```json
     {
       "name": "Test User",
       "email": "test@example.com",
       "password": "test123456"
     }
     ```
   - Click "Execute"

4. **Test Login:**
   - Find `POST /api/auth/login/json`
   - Click "Try it out"
   - Enter credentials:
     ```json
     {
       "email": "test@example.com",
       "password": "test123456"
     }
     ```
   - Copy the `access_token` from the response

5. **Test Protected Endpoint:**
   - Find `GET /api/auth/me`
   - Click "Try it out"
   - Click the "Authorize" button at the top
   - Enter: `Bearer <your_access_token>`
   - Click "Authorize" and "Close"
   - Click "Execute" - You should see your user info

### Using cURL

**Register:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123456"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123456"
  }'
```

**Get Current User (replace TOKEN with actual token):**
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer TOKEN"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
register_data = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123456"
}
response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
print("Register:", response.json())

# Login
login_data = {
    "email": "test@example.com",
    "password": "test123456"
}
response = requests.post(f"{BASE_URL}/api/auth/login/json", json=login_data)
token = response.json()["access_token"]
print("Token:", token)

# Get Current User
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
print("Current User:", response.json())
```

## 🔒 Security Features

1. **Password Hashing**: Passwords are never stored in plain text
2. **JWT Tokens**: Stateless authentication with expiration
3. **Role-Based Access**: Admin endpoints protected
4. **Input Validation**: Pydantic schemas validate all inputs
5. **Error Handling**: Proper HTTP status codes and error messages
6. **OAuth2 Standard**: Follows OAuth2 password flow for compatibility

## 📝 Environment Variables

Make sure your `.env` file has:
```env
SECRET_KEY=your-secret-key-here  # Change this to a random string!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important**: Generate a secure SECRET_KEY for production:
```python
import secrets
print(secrets.token_urlsafe(32))
```

## 🎯 Next Steps (Step 3: Issue CRUD Endpoints)

In the next step, we'll implement:

1. ✅ Create issue endpoint (POST)
2. ✅ Get all issues endpoint (GET)
3. ✅ Get issue by ID endpoint (GET)
4. ✅ Update issue status endpoint (PUT/PATCH, admin only)
5. ✅ Delete issue endpoint (DELETE, admin only)
6. ✅ Image upload handling
7. ✅ File storage and path management

---

**Status**: Step 2 Complete ✅
**Ready for**: Step 3 - Issue CRUD Endpoints

