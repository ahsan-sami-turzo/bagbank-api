# BagBank Backend API

A FastAPI-based backend for managing bag business operations with PostgreSQL database and JWT authentication.

## Features

- **User Authentication**: JWT-based authentication with role-based access control
- **User Roles**: Superadmin, Admin, and Moderator roles
- **PostgreSQL Integration**: Robust database connection with SQLAlchemy ORM
- **CORS Support**: Ready for React frontend integration
- **Environment Configuration**: Secure configuration management

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

1. **Clone the repository** (if not already done)
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   - Create a database named `bagbankdb`
   - Update database credentials in `.env` file if needed

5. **Create environment file**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   # Edit .env with your database credentials
   ```

6. **Initialize the database**
   ```bash
   python init_db.py
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

2. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## Default Users

The system comes with three default users:

| Username | Password | Role |
|----------|----------|------|
| superadmin | bbsuperadmin | Superadmin |
| admin | bbadmin | Admin |
| bbmoderator | bbmoderator | Moderator |

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - User logout

### Example Login Request
```json
{
  "username": "admin",
  "password": "bbadmin"
}
```

### Example Login Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

## Project Structure

```
backend/
├── app/
│   ├── core/           # Core configuration and database
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── utils/          # Utility functions
│   └── api/            # API routes
├── main.py             # FastAPI application
├── init_db.py          # Database initialization
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bagbankdb
DB_USER=postgres
DB_PASSWORD=your_password

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
ALLOWED_HOSTS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Environment
ENVIRONMENT=development
```

## Development

- The application uses SQLAlchemy ORM for database operations
- JWT tokens are used for authentication
- Password hashing is done using bcrypt
- CORS is configured for React frontend integration

## Next Steps

1. Set up your React frontend
2. Implement additional business logic
3. Add more user management features
4. Implement product catalog management
5. Add order management system

