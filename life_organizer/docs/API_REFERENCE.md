# 📚 LIFE ORGANIZER - Complete API Reference

## 🔗 Base URL
```
Production: https://api.lifeorganizer.app
Development: http://localhost:8000/api
```

## 🔐 Authentication

All API endpoints (except registration and login) require JWT authentication.

### Headers
```http
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

### Token Refresh
Tokens expire after 60 minutes. Use the refresh token to get a new access token.

---

## 👤 Authentication Endpoints

### Register User
```http
POST /auth/register/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

**Response (201):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2025-07-06T18:18:40.716617Z"
  }
}
```

### Login
```http
POST /auth/login/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

### Logout
```http
POST /auth/logout/
```

**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

### Get Current User
```http
GET /auth/me/
```

### Change Password
```http
POST /auth/change-password/
```

**Request Body:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass123",
  "new_password_confirm": "newpass123"
}
```

---

## 💰 Expense Management

### Categories

#### Get Expense Categories
```http
GET /expenses/categories/
```

#### Create Default Categories
```http
POST /expenses/categories/create_defaults/
```

#### Create Custom Category
```http
POST /expenses/categories/
```

**Request Body:**
```json
{
  "name": "Entertainment",
  "description": "Movies, games, etc.",
  "icon": "movie",
  "color": "#FF9800"
}
```

### Transactions

#### Get Transactions
```http
GET /expenses/transactions/
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `transaction_type`: `income` or `expense`
- `start_date`: YYYY-MM-DD format
- `end_date`: YYYY-MM-DD format
- `search`: Search in description/notes

#### Create Transaction
```http
POST /expenses/transactions/
```

**Request Body:**
```json
{
  "transaction_type": "expense",
  "amount": 25.50,
  "description": "Coffee and pastry",
  "notes": "Morning coffee at Starbucks",
  "expense_category": 1,
  "transaction_date": "2025-07-06T09:30:00Z",
  "location": "Downtown Starbucks"
}
```

#### Get Recent Transactions
```http
GET /expenses/transactions/recent/
```

#### Get Transaction Summary
```http
GET /expenses/transactions/summary/
```

**Query Parameters:**
- `start_date`: YYYY-MM-DD
- `end_date`: YYYY-MM-DD

**Response:**
```json
{
  "total_income": 2500.00,
  "total_expenses": 1234.56,
  "net_amount": 1265.44,
  "transaction_count": 45,
  "period": "month"
}
```

### Analytics

#### Get Expense Analytics
```http
GET /expenses/analytics/
```

**Response:**
```json
{
  "period": {
    "start_date": "2025-07-01",
    "end_date": "2025-07-31"
  },
  "category_breakdown": [
    {
      "category_name": "Food & Dining",
      "category_color": "#FF5722",
      "total_amount": 450.75,
      "transaction_count": 23,
      "percentage": 36.5
    }
  ],
  "monthly_trends": [
    {
      "month": "Jun 2025",
      "income": 2500.00,
      "expenses": 1200.00,
      "net": 1300.00
    }
  ]
}
```

---

## 📋 Task Management

### Projects

#### Get Projects
```http
GET /tasks/projects/
```

#### Create Project
```http
POST /tasks/projects/
```

**Request Body:**
```json
{
  "name": "Website Redesign",
  "description": "Complete redesign of company website",
  "workspace": 1,
  "color": "#2196F3",
  "start_date": "2025-07-01",
  "end_date": "2025-09-30"
}
```

### Tasks

#### Get Tasks
```http
GET /tasks/tasks/
```

**Query Parameters:**
- `status`: `todo`, `in_progress`, `review`, `done`
- `priority`: `low`, `medium`, `high`, `urgent`
- `project`: Project ID
- `assignee`: User ID

#### Create Task
```http
POST /tasks/tasks/
```

**Request Body:**
```json
{
  "title": "Design homepage mockup",
  "description": "Create wireframes and mockups for new homepage",
  "project": 1,
  "workspace": 1,
  "priority": "high",
  "status": "todo",
  "due_date": "2025-07-15T17:00:00Z",
  "estimated_hours": 8,
  "tags": "design,homepage,mockup"
}
```

#### Get My Tasks
```http
GET /tasks/tasks/my_tasks/
```

**Query Parameters:**
- `status`: Filter by status
- `due`: `today`, `overdue`, `upcoming`

#### Get Task Summary
```http
GET /tasks/tasks/summary/
```

**Response:**
```json
{
  "total_tasks": 25,
  "completed_tasks": 15,
  "pending_tasks": 8,
  "overdue_tasks": 2,
  "completion_rate": 60.0
}
```

#### Start/Stop Timer
```http
POST /tasks/tasks/{id}/start_timer/
POST /tasks/tasks/{id}/stop_timer/
```

### Kanban Board
```http
GET /tasks/kanban/
```

**Query Parameters:**
- `project`: Filter by project ID

**Response:**
```json
[
  {
    "status": "todo",
    "title": "To Do",
    "tasks": [...],
    "task_count": 5
  },
  {
    "status": "in_progress",
    "title": "In Progress",
    "tasks": [...],
    "task_count": 3
  }
]
```

### Calendar View
```http
GET /tasks/calendar/
```

**Query Parameters:**
- `month`: Month number (1-12)
- `year`: Year (YYYY)

---

## 🎯 Goal Management

### Categories

#### Create Default Goal Categories
```http
POST /goals/categories/create_defaults/
```

### Goals

#### Get Goals
```http
GET /goals/goals/
```

#### Create Goal
```http
POST /goals/goals/
```

**Request Body:**
```json
{
  "title": "Read 12 books this year",
  "description": "Improve knowledge through reading",
  "category": 1,
  "goal_type": "numeric",
  "status": "active",
  "target_value": 12,
  "current_value": 3,
  "unit": "books",
  "start_date": "2025-01-01",
  "target_date": "2025-12-31",
  "frequency": "yearly"
}
```

#### Get Active Goals
```http
GET /goals/goals/active/
```

#### Get Goal Summary
```http
GET /goals/goals/summary/
```

#### Update Goal Progress
```http
POST /goals/goals/{id}/update_progress/
```

**Request Body:**
```json
{
  "value": 4,
  "notes": "Finished reading 'The Pragmatic Programmer'",
  "completed": false
}
```

### Analytics

#### Get Goal Analytics
```http
GET /goals/analytics/
```

#### Get AI Suggestions
```http
GET /goals/suggestions/
```

**Response:**
```json
{
  "suggestions": [
    {
      "message": "Break down 'Learn Python' into smaller, actionable steps",
      "insight_type": "planning",
      "goal_id": 5,
      "action_suggestion": "Create 3-5 milestones for this goal"
    }
  ],
  "total_active_goals": 8
}
```

#### Get Habit Tracking
```http
GET /goals/habits/
```

**Response:**
```json
{
  "habits": [
    {
      "habit_name": "Daily Exercise",
      "current_streak": 7,
      "longest_streak": 15,
      "completion_rate": 85.7,
      "weekly_progress": [
        {"date": "2025-07-01", "completed": true},
        {"date": "2025-07-02", "completed": true}
      ]
    }
  ]
}
```

---

## 📊 Dashboard

### Overview
```http
GET /dashboard/overview/
```

**Response:**
```json
{
  "total_income": 2500.00,
  "total_expenses": 1234.56,
  "net_amount": 1265.44,
  "budget_used_percentage": 68.5,
  "total_tasks": 25,
  "completed_tasks": 15,
  "pending_tasks": 8,
  "overdue_tasks": 2,
  "total_goals": 10,
  "active_goals": 7,
  "completed_goals": 3,
  "average_goal_progress": 45.2,
  "recent_transactions": [...],
  "upcoming_tasks": [...],
  "goal_milestones": [...]
}
```

### Quick Stats
```http
GET /dashboard/quick-stats/
```

**Query Parameters:**
- `period`: `week`, `month`, `year`

### Widgets

#### Get Dashboard Widgets
```http
GET /dashboard/widgets/
```

#### Reset Dashboard Layout
```http
POST /dashboard/widgets/reset_layout/
```

#### Get Widget Data
```http
GET /dashboard/widgets/widget_data/
```

### Notifications

#### Get Notifications
```http
GET /dashboard/notifications/
```

#### Mark as Read
```http
POST /dashboard/notifications/{id}/mark_read/
```

#### Mark All as Read
```http
POST /dashboard/notifications/mark_all_read/
```

---

## 📈 Error Handling

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

### Error Response Format
```json
{
  "error": "Error message",
  "details": {
    "field_name": ["Field-specific error message"]
  }
}
```

---

## 🔄 Pagination

List endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Response Format:**
```json
{
  "count": 150,
  "next": "http://api.example.com/endpoint/?page=3",
  "previous": "http://api.example.com/endpoint/?page=1",
  "results": [...]
}
```

---

## 🔍 Filtering and Search

Most list endpoints support:
- **Filtering**: Use field names as query parameters
- **Search**: Use `search` parameter for text search
- **Ordering**: Use `ordering` parameter (prefix with `-` for descending)

**Example:**
```http
GET /tasks/tasks/?status=todo&priority=high&search=design&ordering=-created_at
```

---

## 📝 Interactive Documentation

Visit the interactive API documentation:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/
