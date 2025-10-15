# Expense Tracker API

A RESTful API for managing personal expenses with JWT authentication, built with Flask and PostgreSQL.

**Project URL:** https://roadmap.sh/projects/expense-tracker-api

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Expense Categories](#expense-categories)
- [Filter Options](#filter-options)
- [Postman Collection](#postman-collection)
- [Error Handling](#error-handling)

## Features

- User authentication (Sign up & Login)
- JWT-based authentication with access & refresh tokens
- Token refresh mechanism with blacklist
- CRUD operations for expenses
- Expense filtering by date ranges:
  - Past week (7 days)
  - Past month (30 days)
  - Last 3 months (90 days)
  - Custom date range
- User-specific expense isolation
- Password hashing with Werkzeug
- Admin role support
- Comprehensive error handling

## Tech Stack

- **Framework:** Flask 3.x
- **API Documentation:** Flask-Smorest (OpenAPI/Swagger)
- **Database:** PostgreSQL (via Neon)
- **ORM:** SQLAlchemy
- **Authentication:** Flask-JWT-Extended
- **Password Hashing:** Werkzeug
- **Environment Management:** python-dotenv


## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL database (or Neon account)
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd expense_traker_poc
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

6. **Access Swagger UI**
   ```
   http://localhost:5000/swagger-ui
   ```

## Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@host:port/database
CURRENT_API_VERSION=/api/v1
JWT_SECRET=your-super-secret-key-change-this
ADMIN_EMAIL=admin@example.com
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `CURRENT_API_VERSION` | API version prefix | Yes |
| `JWT_SECRET` | Secret key for JWT signing | Yes |
| `ADMIN_EMAIL` | Email for admin privileges | No |

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/signup` | Register new user | No |
| POST | `/api/v1/login` | Login & get tokens | No |
| POST | `/api/v1/refresh-token` | Refresh access token | Yes (Refresh Token) |

### Expenses

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/create-expense` | Create new expense | Yes (Fresh) |
| PUT | `/api/v1/update-expense` | Update existing expense | Yes (Fresh) |
| DELETE | `/api/v1/delete-expense` | Delete expense | Yes (Fresh) |
| GET | `/api/v1/filter-expense` | Get filtered expenses | Yes |

## Authentication

### Sign Up

**Request:**
```bash
POST /api/v1/signup
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "status": true,
  "data": {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com",
    "createdAt": "2025-01-15T10:30:00",
    "updatedAt": "2025-01-15T10:30:00"
  }
}
```

### Login

**Request:**
```bash
POST /api/v1/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "status": true,
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "data": {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

### Refresh Token

**Request:**
```bash
POST /api/v1/refresh-token
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Using JWT Tokens

Include the access token in the Authorization header:

```bash
Authorization: Bearer <access_token>
```

## Expense Operations

### Create Expense

**Request:**
```bash
POST /api/v1/create-expense
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Grocery Shopping",
  "amount": 150.75,
  "category": "Groceries",
  "description": "Weekly groceries from Walmart"
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Grocery Shopping",
  "amount": 150.75,
  "category": "groceries",
  "description": "Weekly groceries from Walmart",
  "user_id": "uuid",
  "createdAt": "2025-01-15T10:30:00",
  "updatedAt": "2025-01-15T10:30:00"
}
```

### Update Expense

**Request:**
```bash
PUT /api/v1/update-expense
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "expense_id": "uuid",
  "title": "Updated Grocery Shopping",
  "amount": 175.50,
  "category": "Groceries",
  "description": "Updated description"
}
```

### Delete Expense

**Request:**
```bash
DELETE /api/v1/delete-expense
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "expense_id": "uuid"
}
```

### Filter Expenses

**Past Week (Default):**
```bash
GET /api/v1/filter-expense
Authorization: Bearer <access_token>
```

**Past Month:**
```bash
GET /api/v1/filter-expense?filter_category=past_month
Authorization: Bearer <access_token>
```

**Last 3 Months:**
```bash
GET /api/v1/filter-expense?filter_category=last_three_month
Authorization: Bearer <access_token>
```

**Custom Date Range:**
```bash
GET /api/v1/filter-expense?filter_category=custom&from_date=2025-01-01&to_date=2025-01-31
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "status": true,
  "data": [
    {
      "id": "uuid",
      "title": "Grocery Shopping",
      "amount": 150.75,
      "category": "groceries",
      "description": "Weekly groceries",
      "user_id": "uuid",
      "createdAt": "2025-01-15T10:30:00",
      "updatedAt": "2025-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

## Expense Categories

The API supports the following expense categories:

- **Groceries** - Food and household items
- **Leisure** - Entertainment and recreation
- **Electronics** - Electronic devices and accessories
- **Utilities** - Bills and utility payments
- **Clothing** - Apparel and fashion
- **Health** - Medical and health-related expenses
- **Others** - Miscellaneous expenses

Categories are case-insensitive. Unknown categories default to "Others".

## Filter Options

| Filter | Value | Description |
|--------|-------|-------------|
| Past Week | `past_week` | Last 7 days (default) |
| Past Month | `past_month` | Last 30 days |
| Last 3 Months | `last_three_month` | Last 90 days |
| Custom Range | `custom` | Specify `from_date` & `to_date` |

**Date Format:** ISO 8601 format
- `YYYY-MM-DD` (e.g., `2025-01-15`)
- `YYYY-MM-DDTHH:MM:SS` (e.g., `2025-01-15T10:30:00`)

## Postman Collection

Import the provided Postman collection for easy API testing:

1. Open Postman
2. Click **Import**
3. Select `Expense_Tracker_API.postman_collection.json`
4. Collection includes:
   - Pre-configured requests
   - Auto token management
   - Environment variables setup
   - Test scripts for automation

**Environment Variables:**
- `base_url` - API base URL (default: `http://localhost:5000`)
- `access_token` - Auto-populated on login
- `refresh_token` - Auto-populated on login
- `expense_id` - Auto-populated on expense creation

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "status": false,
  "error": "title is missing"
}
```

**401 Unauthorized:**
```json
{
  "message": "The token has expired.",
  "error": "token_expired"
}
```

**404 Not Found:**
```json
{
  "status": false,
  "error": "expense not found"
}
```

**500 Internal Server Error:**
```json
{
  "status": false,
  "error": "Failed to create expense: <error details>"
}
```

### JWT Error Types

| Error | Description |
|-------|-------------|
| `token_expired` | Access token has expired, use refresh token |
| `fresh_token_required` | Operation requires fresh token (re-login) |
| `invalid_token` | Token signature verification failed |
| `authorization_required` | No token provided |
| `token_revoked` | Token has been blacklisted |

## = Security Features

- Password hashing using Werkzeug
- JWT token-based authentication
- Token refresh mechanism
- Token blacklist for logout
- Fresh token requirement for sensitive operations
- User-specific data isolation
- Admin role support via claims
- Environment-based configuration

## Testing

### Manual Testing with cURL

**Sign Up:**
```bash
curl -X POST http://localhost:5000/api/v1/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test123!"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

**Create Expense:**
```bash
curl -X POST http://localhost:5000/api/v1/create-expense \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"title":"Coffee","amount":5.50,"category":"Leisure","description":"Morning coffee"}'
```

## Database Schema

### Users Table
```sql
users (
  id: UUID PRIMARY KEY,
  username: VARCHAR(255) NOT NULL,
  email: VARCHAR(255) NOT NULL UNIQUE,
  password: VARCHAR(255) NOT NULL,
  createdAt: TIMESTAMP,
  updatedAt: TIMESTAMP
)
```

### Expenses Table
```sql
expenses (
  id: UUID PRIMARY KEY,
  title: VARCHAR(255) NOT NULL,
  amount: FLOAT NOT NULL,
  category: VARCHAR(255) NOT NULL,
  description: VARCHAR(255),
  user_id: UUID FOREIGN KEY REFERENCES users(id),
  createdAt: TIMESTAMP,
  updatedAt: TIMESTAMP
)
```

## Contributing

This project is part of the [roadmap.sh Backend Projects](https://roadmap.sh/projects/expense-tracker-api). Contributions are welcome!

## License

This project is open source and available for educational purposes.

## Project Requirements Met

 - User sign up and login
 - JWT generation and validation
 - Protected API endpoints
 - CRUD operations for expenses
 - Expense filtering (past week, month, 3 months, custom)
 - Predefined expense categories
 - User-specific expense management
 - Token refresh mechanism
 - Comprehensive error handling
 - API documentation (Swagger UI)

---

**Built as part of the Backend Developer Roadmap** - https://roadmap.sh/projects/expense-tracker-api
