# LIFE ORGANIZER - API Integration Guide

## 🎯 Overview

This guide demonstrates how the Flutter frontend integrates with the Django backend API. The integration includes authentication, expense management, and real-time data synchronization.

## 🔐 Authentication Flow

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

**Response:**
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

### 2. User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

### 3. Protected Endpoints
All subsequent API calls require the JWT token in the Authorization header:
```bash
curl -X GET http://localhost:8000/api/expenses/categories/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## 💰 Expense Management API

### 1. Create Default Categories
```bash
curl -X POST http://localhost:8000/api/expenses/categories/create_defaults/ \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "message": "Created 8 default categories",
  "categories": [
    {
      "id": 1,
      "name": "Food & Dining",
      "icon": "restaurant",
      "color": "#FF5722",
      "total_spent": 0.0,
      "transaction_count": 0
    }
  ]
}
```

### 2. Add Transaction
```bash
curl -X POST http://localhost:8000/api/expenses/transactions/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "expense",
    "amount": 25.50,
    "description": "Lunch at restaurant",
    "expense_category": 1,
    "transaction_date": "2025-07-06T12:30:00Z"
  }'
```

### 3. Get Transaction Summary
```bash
curl -X GET "http://localhost:8000/api/expenses/transactions/summary/?start_date=2025-07-01&end_date=2025-07-31" \
  -H "Authorization: Bearer <token>"
```

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

## 📱 Frontend Integration

### 1. Authentication Service
The Flutter app uses Riverpod for state management and Dio for HTTP requests:

```dart
// Login example
await ref.read(authStateProvider.notifier).login(
  username,
  password,
);

// The auth state automatically updates and triggers navigation
ref.listen<AuthState>(authStateProvider, (previous, next) {
  if (next.isAuthenticated) {
    context.go(AppRoutes.dashboard);
  }
});
```

### 2. Expense Service
```dart
// Get expense categories
final categories = await ref.read(expenseServiceProvider).getExpenseCategories();

// Create transaction
final transaction = await ref.read(expenseServiceProvider).createTransaction(
  type: TransactionType.expense,
  amount: 25.50,
  description: 'Lunch',
  expenseCategoryId: 1,
);
```

### 3. Error Handling
The app includes comprehensive error handling:

```dart
try {
  await expenseService.createTransaction(...);
} catch (e) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text(e.toString())),
  );
}
```

## 🔄 Data Flow

### 1. Authentication Flow
1. User enters credentials in Flutter app
2. App sends POST request to `/api/auth/login/`
3. Backend validates credentials and returns JWT tokens
4. App stores tokens securely using FlutterSecureStorage
5. All subsequent requests include Bearer token in headers

### 2. Data Synchronization
1. App fetches data from API on startup
2. Data is cached locally using Hive for offline access
3. User actions trigger API calls to update backend
4. Local cache is updated on successful API responses
5. Error states are handled gracefully with retry mechanisms

### 3. Real-time Updates
- JWT tokens are automatically refreshed before expiration
- API interceptors handle token refresh transparently
- Network errors trigger offline mode with cached data

## 🧪 Testing the Integration

### 1. Start the Backend
```bash
cd life_organizer/backend
python manage.py runserver 0.0.0.0:8000
```

### 2. Test API Endpoints
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "first_name": "Test", "last_name": "User", "password": "testpass123", "password_confirm": "testpass123"}'

# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' | \
  python -c "import sys, json; print(json.load(sys.stdin)['access'])")

# Create default categories
curl -X POST http://localhost:8000/api/expenses/categories/create_defaults/ \
  -H "Authorization: Bearer $TOKEN"

# Get categories
curl -X GET http://localhost:8000/api/expenses/categories/ \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Test Frontend (when Flutter is available)
```bash
cd life_organizer/frontend
flutter run -d web
```

## 📊 API Documentation

The backend provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔧 Configuration

### Backend Configuration
- **Base URL**: `http://localhost:8000/api`
- **JWT Access Token Lifetime**: 60 minutes
- **JWT Refresh Token Lifetime**: 7 days
- **CORS**: Enabled for frontend origins

### Frontend Configuration
- **API Base URL**: Configurable in `app_constants.dart`
- **Token Storage**: Secure storage for sensitive data
- **Cache Duration**: 5 minutes for API responses
- **Timeout**: 30 seconds for API requests

## 🚀 Deployment Considerations

### Backend
- Use environment variables for sensitive settings
- Configure proper CORS origins for production
- Set up HTTPS with SSL certificates
- Use PostgreSQL for production database

### Frontend
- Update API base URL for production
- Enable web app manifest for PWA features
- Configure proper error tracking
- Optimize build for production deployment

## 🔮 Next Steps

1. **Implement remaining modules** (Tasks, Goals, Dashboard)
2. **Add real-time notifications** using WebSockets
3. **Implement offline synchronization** with conflict resolution
4. **Add comprehensive testing** (unit, integration, e2e)
5. **Set up CI/CD pipeline** for automated deployment
6. **Add performance monitoring** and analytics
7. **Implement advanced features** (voice input, file uploads, etc.)

This integration provides a solid foundation for a full-featured personal life organizer application with modern architecture and best practices.
