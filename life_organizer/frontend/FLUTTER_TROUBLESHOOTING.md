# 🔧 Flutter Troubleshooting Guide

## 🚨 Common Flutter Run Errors & Solutions

### 1. **Quick Test - Simple Version**

If you're getting errors with the main app, try the simplified version first:

```bash
cd life_organizer/frontend
# Rename main files temporarily
mv lib/main.dart lib/main_complex.dart
mv lib/main_simple.dart lib/main.dart

# Run the simple version
flutter clean
flutter pub get
flutter run -d web
```

This will run a basic version with minimal dependencies to test if Flutter itself is working.

### 2. **Diagnosis Script**

Run the comprehensive diagnosis script:

```bash
cd life_organizer/frontend
python diagnose_flutter_errors.py
```

This will check for:
- Missing imports
- Dependency issues
- Common Flutter problems
- File structure issues

### 3. **Common Error Solutions**

#### **Error: "Package not found" or Import Issues**

```bash
# Clean and reinstall dependencies
flutter clean
flutter pub get
flutter pub deps
```

#### **Error: "Web support not enabled"**

```bash
# Enable web support
flutter config --enable-web
flutter create . --platforms web
```

#### **Error: "SDK version issues"**

Check your Flutter version:
```bash
flutter --version
flutter doctor
```

Make sure you have:
- Flutter SDK 3.10.0 or higher
- Dart SDK 3.0.0 or higher

#### **Error: "go_router" or "flutter_riverpod" issues**

```bash
# Update dependencies
flutter pub upgrade
flutter pub get
```

#### **Error: "Hive" or storage issues**

The main.dart has been updated to handle storage initialization errors. If you still get issues:

```bash
# Remove problematic dependencies temporarily
# Edit pubspec.yaml and comment out:
# - hive
# - hive_flutter
# - flutter_secure_storage
```

### 4. **Step-by-Step Debugging**

#### **Step 1: Basic Flutter Check**
```bash
flutter doctor -v
```
Ensure all checkmarks are green or yellow (not red).

#### **Step 2: Clean Build**
```bash
flutter clean
rm -rf build/
flutter pub get
```

#### **Step 3: Verbose Run**
```bash
flutter run -d web --verbose
```
This will show detailed error messages.

#### **Step 4: Analyze Code**
```bash
flutter analyze
dart analyze
```

### 5. **Specific Error Messages**

#### **"Failed to load asset" errors**
- Check `pubspec.yaml` for asset references
- Ensure asset files exist or comment out missing assets

#### **"RenderFlex overflowed" errors**
- UI layout issues - usually safe to ignore during development
- Add `Expanded` or `Flexible` widgets around problematic widgets

#### **"Provider not found" errors**
- Ensure `ProviderScope` is at the root of the app
- Check that providers are properly defined

#### **"Navigator" or routing errors**
- Try the simplified router configuration
- Check that all route paths are properly defined

### 6. **Alternative Testing Methods**

#### **Method 1: Use Simple Version**
```bash
# Use the minimal version
mv lib/main.dart lib/main_complex.dart
mv lib/main_simple.dart lib/main.dart
flutter run -d web
```

#### **Method 2: Progressive Testing**
1. Start with simple MaterialApp
2. Add Riverpod
3. Add routing
4. Add complex widgets

#### **Method 3: Platform Testing**
```bash
# Try different platforms
flutter run -d chrome
flutter run -d web-server --web-port 8080
```

### 7. **Environment Setup**

#### **Required Tools:**
- Flutter SDK 3.10.0+
- Dart SDK 3.0.0+
- Chrome browser (for web)
- Git

#### **Installation Check:**
```bash
flutter doctor
flutter config --enable-web
flutter devices
```

### 8. **Common pubspec.yaml Issues**

Check your `pubspec.yaml` for:
- Correct indentation (use spaces, not tabs)
- Valid version numbers
- No conflicting dependencies

#### **Minimal Working pubspec.yaml:**
```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
```

### 9. **Emergency Fallback**

If nothing works, create a new Flutter project:

```bash
# Create new project
flutter create life_organizer_test
cd life_organizer_test

# Copy your lib files
cp -r ../life_organizer/frontend/lib/* lib/

# Use minimal pubspec.yaml
flutter pub get
flutter run -d web
```

### 10. **Getting Help**

When asking for help, provide:

1. **Exact error message**
2. **Flutter doctor output**
3. **pubspec.yaml content**
4. **Steps you've tried**

#### **Useful Commands for Debugging:**
```bash
# Get detailed info
flutter doctor -v
flutter --version
flutter analyze
flutter pub deps

# Clean everything
flutter clean
flutter pub get

# Verbose output
flutter run -d web --verbose
```

### 11. **Success Indicators**

You'll know it's working when you see:
- ✅ "Flutter run" starts without errors
- ✅ Web browser opens automatically
- ✅ App loads with navigation bar
- ✅ You can switch between Dashboard, Expenses, Tasks, Goals

### 12. **Next Steps After Success**

Once the app runs:
1. Test navigation between screens
2. Try the different features
3. Check browser console for any warnings
4. Test responsive design by resizing browser

---

## 🎯 **Quick Fix Checklist**

- [ ] Run `flutter doctor` - all green/yellow
- [ ] Run `flutter clean && flutter pub get`
- [ ] Try simple version first (`main_simple.dart`)
- [ ] Check error messages with `--verbose`
- [ ] Ensure web support is enabled
- [ ] Check Flutter/Dart versions
- [ ] Try different browser/platform
- [ ] Use diagnosis script
- [ ] Check pubspec.yaml syntax

**If all else fails, share the specific error message for targeted help!** 🚀
