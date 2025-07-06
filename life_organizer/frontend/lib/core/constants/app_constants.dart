class AppConstants {
  // App Information
  static const String appName = 'Life Organizer';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  static const String baseUrl = 'http://localhost:8000/api';
  static const String authEndpoint = '/auth';
  static const String expensesEndpoint = '/expenses';
  static const String tasksEndpoint = '/tasks';
  static const String goalsEndpoint = '/goals';
  static const String dashboardEndpoint = '/dashboard';
  
  // Storage Keys
  static const String authTokenKey = 'auth_token';
  static const String userDataKey = 'user_data';
  static const String themeKey = 'theme_preference';
  static const String languageKey = 'language_preference';
  
  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;
  
  // File Upload
  static const int maxFileSize = 10 * 1024 * 1024; // 10MB
  static const List<String> allowedImageTypes = ['jpg', 'jpeg', 'png', 'gif'];
  static const List<String> allowedDocumentTypes = ['pdf', 'doc', 'docx', 'txt'];
  
  // Validation
  static const int minPasswordLength = 8;
  static const int maxDescriptionLength = 500;
  static const int maxTitleLength = 100;
  
  // Animation Durations
  static const Duration shortAnimation = Duration(milliseconds: 200);
  static const Duration mediumAnimation = Duration(milliseconds: 300);
  static const Duration longAnimation = Duration(milliseconds: 500);
  
  // Timeouts
  static const Duration apiTimeout = Duration(seconds: 30);
  static const Duration connectionTimeout = Duration(seconds: 10);
  
  // Currency
  static const String defaultCurrency = 'USD';
  static const List<String> supportedCurrencies = ['USD', 'EUR', 'GBP', 'JPY'];
  
  // Date Formats
  static const String dateFormat = 'yyyy-MM-dd';
  static const String dateTimeFormat = 'yyyy-MM-dd HH:mm:ss';
  static const String displayDateFormat = 'MMM dd, yyyy';
  static const String displayTimeFormat = 'HH:mm';
}
