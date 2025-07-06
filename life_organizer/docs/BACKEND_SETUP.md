# LIFE ORGANIZER - Backend Setup Documentation

## 🎯 Overview

The LIFE ORGANIZER backend is built with Django and Django REST Framework, providing a comprehensive API for personal life management including expense tracking, task management, goal planning, and dashboard analytics.

## 🏗️ Architecture

### Core Applications

1. **users** - User authentication, profiles, and workspaces
2. **expenses** - Expense tracking, budgets, and financial analytics
3. **tasks** - Task management, projects, and time tracking
4. **goals** - Personal goal setting, progress tracking, and journaling
5. **dashboard** - Dashboard widgets, notifications, and user preferences

### Database Models

#### Users App
- `UserProfile` - Extended user information and preferences
- `Workspace` - Organize tasks and goals by context (Personal/Work/Team)

#### Expenses App
- `ExpenseCategory` / `IncomeCategory` - Categorization system
- `Transaction` - All financial transactions (income/expenses)
- `Budget` - Monthly budgets with alerts
- `BudgetAlert` - Automated budget notifications

#### Tasks App
- `Project` - Group related tasks
- `Task` - Main task entity with hierarchy support
- `TaskComment` - Task discussions
- `TaskAttachment` - File attachments
- `TaskReminder` - Automated reminders
- `TaskTimeLog` - Time tracking

#### Goals App
- `GoalCategory` - Goal organization
- `Goal` - Personal objectives with progress tracking
- `GoalProgress` - Daily/weekly progress entries
- `GoalMilestone` - Break down large goals
- `JournalEntry` - Daily reflections
- `MonthlyReview` - Monthly goal reviews

#### Dashboard App
- `DashboardWidget` - Configurable dashboard components
- `Notification` - System notifications
- `UserActivity` - Activity tracking for analytics
- `DashboardPreference` - User customization settings

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Django 5.2.4
- PostgreSQL (recommended for production)

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd life_organizer/backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/me/` - Current user info

#### Expenses
- `GET/POST /api/expenses/transactions/` - Transaction CRUD
- `GET/POST /api/expenses/categories/` - Expense categories
- `GET/POST /api/expenses/budgets/` - Budget management
- `GET /api/expenses/analytics/` - Expense analytics

#### Tasks
- `GET/POST /api/tasks/tasks/` - Task CRUD
- `GET/POST /api/tasks/projects/` - Project management
- `GET /api/tasks/kanban/` - Kanban board view
- `GET /api/tasks/calendar/` - Calendar view

#### Goals
- `GET/POST /api/goals/goals/` - Goal CRUD
- `GET/POST /api/goals/progress/` - Progress tracking
- `GET/POST /api/goals/journal/` - Journal entries
- `GET /api/goals/analytics/` - Goal analytics

#### Dashboard
- `GET /api/dashboard/overview/` - Dashboard overview
- `GET/POST /api/dashboard/widgets/` - Widget management
- `GET /api/dashboard/notifications/` - User notifications

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📝 Next Steps

1. **Implement API Views** - Create comprehensive ViewSets and serializers
2. **Add Authentication** - JWT token authentication
3. **Create Serializers** - Data validation and serialization
4. **Add Permissions** - User-based access control
5. **Implement Analytics** - Data aggregation and reporting
6. **Add Real-time Features** - WebSocket support for live updates

## 🔧 Configuration

Key settings in `settings.py`:
- Django REST Framework configuration
- CORS settings for frontend integration
- Media file handling for uploads
- Database configuration

## 📊 Features Implemented

✅ Database models for all modules
✅ Django admin interface
✅ Basic URL routing
✅ Migration system
✅ Test framework setup
✅ CORS configuration for frontend

## 🎯 Upcoming Features

- JWT Authentication
- API serializers and views
- Real-time notifications
- File upload handling
- Data analytics endpoints
- Email notifications
- Background task processing
