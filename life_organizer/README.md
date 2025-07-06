# 🌟 LIFE ORGANIZER - Complete Personal Life Management System

[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://djangoproject.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.10+-blue.svg)](https://flutter.dev/)
[![API](https://img.shields.io/badge/API-REST-orange.svg)](http://localhost:8000/api/docs/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive personal life management application built with Django REST Framework backend and Flutter frontend. Manage your expenses, tasks, goals, and get insights through a beautiful dashboard.

## 🎯 Features

### 💰 **Expense Management**
- ✅ Track income and expenses with categories
- ✅ Set monthly budgets with smart alerts
- ✅ Visual analytics and spending insights
- ✅ Receipt image uploads
- ✅ Voice input support
- ✅ Monthly/yearly financial summaries

### 📋 **Task Management**
- ✅ Create projects and organize tasks
- ✅ Kanban board and calendar views
- ✅ Priority levels and due dates
- ✅ Time tracking and productivity analytics
- ✅ Task comments and file attachments
- ✅ Smart reminders and notifications

### 🎯 **Goal Planning**
- ✅ Set SMART goals with progress tracking
- ✅ Habit tracking with streak counters
- ✅ Milestone management
- ✅ AI-powered next step suggestions
- ✅ Personal journal integration
- ✅ Monthly reviews and reflections

### 📊 **Dashboard & Analytics**
- ✅ Customizable dashboard widgets
- ✅ Real-time overview of all modules
- ✅ Productivity and financial health scores
- ✅ Trend analysis and insights
- ✅ Activity feed and notifications
- ✅ Cross-module data correlations

## 🏗️ Architecture

### Backend (Django REST Framework)
```
backend/
├── life_organizer_project/    # Main Django project
├── users/                     # Authentication & user management
├── expenses/                  # Financial tracking
├── tasks/                     # Task & project management
├── goals/                     # Goal setting & tracking
├── dashboard/                 # Analytics & dashboard
└── requirements.txt           # Python dependencies
```

### Frontend (Flutter)
```
frontend/
├── lib/
│   ├── core/                  # Core utilities & configuration
│   ├── features/              # Feature-specific modules
│   ├── shared/                # Shared components & services
│   └── main.dart              # App entry point
├── assets/                    # Images, fonts, icons
└── pubspec.yaml              # Flutter dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Django 5.2.4
- Flutter 3.10+ (optional, for mobile app)
- PostgreSQL (recommended for production)

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd life_organizer
   ```

2. **Set up Python environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure database:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Start development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - Documentation: http://localhost:8000/api/docs/

### Frontend Setup (Optional)

1. **Install Flutter dependencies:**
   ```bash
   cd frontend
   flutter pub get
   ```

2. **Run the app:**
   ```bash
   flutter run -d web  # For web
   flutter run         # For mobile (requires emulator/device)
   ```

## 📚 API Documentation

### Authentication Endpoints
```
POST /api/auth/register/     # User registration
POST /api/auth/login/        # User login
POST /api/auth/logout/       # User logout
GET  /api/auth/me/           # Current user info
POST /api/auth/change-password/  # Change password
```

### Expense Management
```
GET/POST /api/expenses/categories/           # Expense categories
GET/POST /api/expenses/transactions/         # Transactions
GET      /api/expenses/transactions/summary/ # Financial summary
GET      /api/expenses/analytics/            # Expense analytics
GET/POST /api/expenses/budgets/              # Budget management
```

### Task Management
```
GET/POST /api/tasks/projects/    # Project management
GET/POST /api/tasks/tasks/       # Task CRUD operations
GET      /api/tasks/kanban/      # Kanban board view
GET      /api/tasks/calendar/    # Calendar view
GET      /api/tasks/analytics/   # Task analytics
```

### Goal Planning
```
GET/POST /api/goals/goals/           # Goal management
GET/POST /api/goals/progress/        # Progress tracking
GET      /api/goals/analytics/       # Goal analytics
GET      /api/goals/suggestions/     # AI suggestions
GET      /api/goals/habits/          # Habit tracking
```

### Dashboard
```
GET /api/dashboard/overview/      # Dashboard overview
GET /api/dashboard/quick-stats/   # Quick statistics
GET /api/dashboard/widgets/       # Widget management
```

## 🧪 Testing

### Complete API Workflow Test

```bash
# 1. Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# 2. Login and get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# 3. Create default categories (use token from login)
curl -X POST http://localhost:8000/api/expenses/categories/create_defaults/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Add a transaction
curl -X POST http://localhost:8000/api/expenses/transactions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "expense",
    "amount": 25.50,
    "description": "Coffee",
    "expense_category": 1
  }'

# 5. View kanban board
curl -X GET http://localhost:8000/api/tasks/kanban/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Production Settings
- Use PostgreSQL database
- Set DEBUG=False
- Configure proper CORS origins
- Set up SSL certificates
- Use environment variables for sensitive data

## 📊 Key Features Demonstrated

### ✅ **Complete CRUD Operations**
- All modules support Create, Read, Update, Delete operations
- Proper data validation and error handling
- User-specific data isolation

### ✅ **Advanced API Features**
- JWT authentication with refresh tokens
- Filtering, searching, and pagination
- Custom actions and endpoints
- Comprehensive error handling

### ✅ **Real-world Functionality**
- Budget alerts and notifications
- Time tracking and productivity metrics
- Goal progress tracking with AI suggestions
- Cross-module analytics and insights

### ✅ **Production-Ready Architecture**
- Clean code organization
- Comprehensive documentation
- Interactive API documentation (Swagger)
- Scalable database design

## 🎨 Frontend Features (Flutter)

### ✅ **Modern UI/UX**
- Material Design 3 components
- Light/Dark theme support
- Responsive design for all screen sizes
- Smooth animations and transitions

### ✅ **State Management**
- Riverpod for reactive state management
- Proper error handling and loading states
- Offline support with local caching
- Real-time data synchronization

### ✅ **Cross-Platform Support**
- Android and iOS mobile apps
- Progressive Web App (PWA)
- Desktop support (Windows, macOS, Linux)

## 🔮 Future Enhancements

- [ ] Real-time notifications with WebSockets
- [ ] Advanced AI insights and recommendations
- [ ] Social features and goal sharing
- [ ] Integration with external services (banks, calendars)
- [ ] Voice commands and natural language processing
- [ ] Advanced data visualization and reporting
- [ ] Multi-language support
- [ ] Offline-first architecture with sync

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- 📧 Email: support@lifeorganizer.app
- 📖 Documentation: [API Docs](http://localhost:8000/api/docs/)
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)

---

**Built with ❤️ using Django REST Framework and Flutter**
