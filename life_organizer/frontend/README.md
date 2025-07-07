# Life Organizer Flutter App

A comprehensive personal life organizer mobile application built with Flutter.

## Features

- 💰 Expense tracking and budget management
- 📋 Task management with Kanban board
- 🎯 Goal setting and progress tracking
- 📊 Analytics and insights dashboard
- 🔐 Secure authentication
- 📱 Cross-platform (iOS, Android, Web)

## Prerequisites

- Flutter SDK 3.10.0 or higher
- Dart SDK 3.0.0 or higher
- Android Studio / VS Code with Flutter extensions
- iOS development: Xcode (for iOS builds)

## Getting Started

1. **Install dependencies:**
   ```bash
   flutter pub get
   ```

2. **Run code generation (if needed):**
   ```bash
   flutter packages pub run build_runner build
   ```

3. **Run the app:**
   ```bash
   # For development
   flutter run
   
   # For web
   flutter run -d web
   
   # For specific device
   flutter run -d <device_id>
   ```

## Project Structure

```
lib/
├── core/                 # Core utilities and configuration
│   ├── constants/        # App constants
│   ├── network/          # API client and interceptors
│   ├── storage/          # Local storage services
│   ├── theme/            # App theme configuration
│   └── utils/            # Utility functions and routing
├── features/             # Feature-specific modules
│   ├── auth/             # Authentication
│   ├── dashboard/        # Dashboard and overview
│   ├── expenses/         # Expense management
│   ├── goals/            # Goal planning
│   └── tasks/            # Task management
├── shared/               # Shared components and services
│   ├── models/           # Data models
│   ├── services/         # API services
│   └── widgets/          # Reusable widgets
└── main.dart             # App entry point
```

## Configuration

### API Configuration

Update the API base URL in `lib/core/constants/app_constants.dart`:

```dart
class AppConstants {
  static const String baseUrl = 'http://localhost:8000/api';
  // For production: 'https://your-api-domain.com/api'
}
```

### Assets

- **Images**: Place image files in `assets/images/`
- **Icons**: Place icon files in `assets/icons/`
- **Fonts**: Place font files in `assets/fonts/`

After adding assets, update `pubspec.yaml` to include them:

```yaml
flutter:
  assets:
    - assets/images/
    - assets/icons/
  
  fonts:
    - family: YourFont
      fonts:
        - asset: assets/fonts/YourFont-Regular.ttf
```

## Building for Production

### Android
```bash
flutter build apk --release
# or for app bundle
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

### Web
```bash
flutter build web --release
```

## Development

### Code Generation

This project uses code generation for models and services. Run the following command when you modify annotated classes:

```bash
flutter packages pub run build_runner build --delete-conflicting-outputs
```

### State Management

The app uses Riverpod for state management. Key concepts:

- **Providers**: Define data sources and business logic
- **ConsumerWidget**: Widgets that listen to providers
- **Ref**: Access providers within widgets

### Testing

Run tests with:
```bash
flutter test
```

## Troubleshooting

### Common Issues

1. **Asset not found errors**: Ensure assets are properly declared in `pubspec.yaml`
2. **Build errors**: Run `flutter clean && flutter pub get`
3. **Code generation issues**: Run `flutter packages pub run build_runner clean`

### Performance

- Use `const` constructors where possible
- Implement proper list view builders for large datasets
- Use `cached_network_image` for network images
- Profile with `flutter run --profile`

## Contributing

1. Follow the existing code structure
2. Use meaningful commit messages
3. Add tests for new features
4. Update documentation as needed

## License

This project is part of the Life Organizer system.
