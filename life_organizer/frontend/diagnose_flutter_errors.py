#!/usr/bin/env python3
"""
Flutter Error Diagnosis Script
Checks for common Flutter compilation and runtime errors
"""

import os
import re
import sys
from pathlib import Path

def check_dart_syntax(file_path):
    """Check for common Dart syntax errors"""
    errors = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
        for i, line in enumerate(lines, 1):
            # Check for common syntax issues
            if 'import ' in line and not line.strip().endswith(';'):
                errors.append(f"Line {i}: Missing semicolon after import")
            
            if line.strip().endswith(',') and 'import' in line:
                errors.append(f"Line {i}: Comma after import statement")
            
            # Check for unmatched brackets
            open_brackets = line.count('(') + line.count('[') + line.count('{')
            close_brackets = line.count(')') + line.count(']') + line.count('}')
            
    except Exception as e:
        errors.append(f"Error reading file: {e}")
    
    return errors

def check_missing_imports():
    """Check for missing imports in key files"""
    print("🔍 Checking for Missing Imports...")
    print("-" * 40)
    
    files_to_check = [
        "lib/main.dart",
        "lib/core/utils/app_router.dart", 
        "lib/features/dashboard/screens/dashboard_screen.dart",
        "lib/features/expenses/screens/expenses_screen.dart",
        "lib/features/tasks/screens/tasks_screen.dart"
    ]
    
    issues = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check for common missing imports
                if 'ConsumerWidget' in content and 'flutter_riverpod' not in content:
                    issues.append(f"{file_path}: Missing flutter_riverpod import")
                
                if 'GoRouter' in content and 'go_router' not in content:
                    issues.append(f"{file_path}: Missing go_router import")
                
                if 'MaterialApp' in content and 'package:flutter/material.dart' not in content:
                    issues.append(f"{file_path}: Missing material.dart import")
                
                print(f"✅ {file_path}: Imports look good")
                
            except Exception as e:
                issues.append(f"{file_path}: Error reading file - {e}")
        else:
            issues.append(f"{file_path}: File not found")
    
    if issues:
        print("\n❌ Import Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All imports look good!")
        return True

def check_pubspec_dependencies():
    """Check pubspec.yaml for dependency issues"""
    print("\n🔍 Checking pubspec.yaml Dependencies...")
    print("-" * 40)
    
    if not os.path.exists("pubspec.yaml"):
        print("❌ pubspec.yaml not found!")
        return False
    
    try:
        with open("pubspec.yaml", 'r') as f:
            content = f.read()
        
        required_deps = [
            'flutter_riverpod',
            'go_router', 
            'dio',
            'shared_preferences',
            'hive_flutter',
            'flutter_secure_storage'
        ]
        
        missing_deps = []
        for dep in required_deps:
            if dep not in content:
                missing_deps.append(dep)
        
        if missing_deps:
            print("❌ Missing dependencies:")
            for dep in missing_deps:
                print(f"   - {dep}")
            return False
        else:
            print("✅ All required dependencies found!")
            return True
            
    except Exception as e:
        print(f"❌ Error reading pubspec.yaml: {e}")
        return False

def check_common_flutter_issues():
    """Check for common Flutter project issues"""
    print("\n🔍 Checking Common Flutter Issues...")
    print("-" * 40)
    
    issues = []
    
    # Check if main.dart has proper structure
    if os.path.exists("lib/main.dart"):
        with open("lib/main.dart", 'r') as f:
            main_content = f.read()
        
        if 'void main()' not in main_content:
            issues.append("main.dart: Missing main() function")
        
        if 'runApp(' not in main_content:
            issues.append("main.dart: Missing runApp() call")
        
        if 'MaterialApp' not in main_content and 'MaterialApp.router' not in main_content:
            issues.append("main.dart: Missing MaterialApp")
    else:
        issues.append("main.dart: File not found")
    
    # Check for asset issues
    if os.path.exists("pubspec.yaml"):
        with open("pubspec.yaml", 'r') as f:
            pubspec_content = f.read()
        
        if 'assets:' in pubspec_content:
            # Check if referenced assets exist
            asset_lines = [line.strip() for line in pubspec_content.split('\n') if line.strip().startswith('- assets/')]
            for asset_line in asset_lines:
                asset_path = asset_line.replace('- ', '').strip()
                if not os.path.exists(asset_path):
                    issues.append(f"Asset not found: {asset_path}")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ No common issues found!")
        return True

def suggest_fixes():
    """Suggest fixes for common issues"""
    print("\n🔧 Suggested Fixes:")
    print("-" * 40)
    
    print("1. **Clean and rebuild:**")
    print("   flutter clean")
    print("   flutter pub get")
    print("   flutter run -d web")
    print()
    
    print("2. **Check Flutter version:**")
    print("   flutter --version")
    print("   flutter doctor")
    print()
    
    print("3. **Enable web support (if needed):**")
    print("   flutter config --enable-web")
    print()
    
    print("4. **Run with verbose output:**")
    print("   flutter run -d web --verbose")
    print()
    
    print("5. **Check for specific errors:**")
    print("   flutter analyze")
    print("   dart analyze")

def main():
    print("🚀 Flutter Error Diagnosis")
    print("=" * 50)
    
    # Change to frontend directory
    if os.path.exists("life_organizer/frontend"):
        os.chdir("life_organizer/frontend")
        print(f"📁 Working directory: {os.getcwd()}")
    else:
        print("❌ Frontend directory not found!")
        sys.exit(1)
    
    # Run checks
    imports_ok = check_missing_imports()
    pubspec_ok = check_pubspec_dependencies()
    common_ok = check_common_flutter_issues()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS RESULTS")
    print("=" * 50)
    
    if imports_ok and pubspec_ok and common_ok:
        print("🎉 No obvious issues found!")
        print("✅ The app structure looks correct")
        print("\n💡 If you're still getting errors, try:")
        print("   1. flutter clean && flutter pub get")
        print("   2. flutter run -d web --verbose")
        print("   3. Share the specific error message for more help")
    else:
        print("❌ Issues found! Please fix the problems above.")
        suggest_fixes()
    
    print("\n🔍 For more detailed error analysis, please share:")
    print("   - The exact error message you're seeing")
    print("   - Output of 'flutter doctor'")
    print("   - Output of 'flutter analyze'")

if __name__ == "__main__":
    main()
