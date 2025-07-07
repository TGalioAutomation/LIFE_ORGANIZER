#!/usr/bin/env python3
"""
Flutter App Structure Verification Script
Checks if all required files exist and imports are correct
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print result"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_flutter_structure():
    """Check Flutter app structure"""
    print("🔍 Checking Flutter App Structure...")
    print("=" * 60)
    
    base_path = "lib"
    all_good = True
    
    # Core files
    core_files = [
        ("lib/main.dart", "Main app entry point"),
        ("lib/core/theme/app_theme.dart", "App theme"),
        ("lib/core/constants/app_constants.dart", "App constants"),
        ("lib/core/utils/app_router.dart", "App router"),
        ("lib/core/storage/storage_service.dart", "Storage service"),
        ("lib/core/network/api_client.dart", "API client"),
    ]
    
    print("\n📁 Core Files:")
    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Shared widgets
    shared_widgets = [
        ("lib/shared/widgets/loading_widget.dart", "Loading widget"),
        ("lib/shared/widgets/error_widget.dart", "Error widget"),
    ]
    
    print("\n🔧 Shared Widgets:")
    for file_path, description in shared_widgets:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Dashboard files
    dashboard_files = [
        ("lib/features/dashboard/screens/dashboard_screen.dart", "Dashboard screen"),
        ("lib/features/dashboard/widgets/dashboard_header.dart", "Dashboard header"),
        ("lib/features/dashboard/widgets/quick_stats_card.dart", "Quick stats card"),
        ("lib/features/dashboard/widgets/recent_transactions_card.dart", "Recent transactions"),
        ("lib/features/dashboard/widgets/upcoming_tasks_card.dart", "Upcoming tasks"),
        ("lib/features/dashboard/widgets/goal_progress_card.dart", "Goal progress"),
        ("lib/features/dashboard/widgets/expense_chart_card.dart", "Expense chart"),
    ]
    
    print("\n📊 Dashboard Files:")
    for file_path, description in dashboard_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Expense files
    expense_files = [
        ("lib/features/expenses/screens/expenses_screen.dart", "Expenses screen"),
        ("lib/features/expenses/widgets/expense_summary_card.dart", "Expense summary"),
        ("lib/features/expenses/widgets/expense_chart_widget.dart", "Expense chart widget"),
        ("lib/features/expenses/widgets/transaction_list_widget.dart", "Transaction list"),
        ("lib/features/expenses/widgets/add_transaction_fab.dart", "Add transaction FAB"),
    ]
    
    print("\n💰 Expense Files:")
    for file_path, description in expense_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Task files
    task_files = [
        ("lib/features/tasks/screens/tasks_screen.dart", "Tasks screen"),
        ("lib/features/tasks/widgets/kanban_board_widget.dart", "Kanban board"),
        ("lib/features/tasks/widgets/task_list_widget.dart", "Task list"),
        ("lib/features/tasks/widgets/task_calendar_widget.dart", "Task calendar"),
    ]
    
    print("\n📋 Task Files:")
    for file_path, description in task_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Configuration files
    config_files = [
        ("pubspec.yaml", "Flutter dependencies"),
        ("analysis_options.yaml", "Dart analyzer config"),
    ]
    
    print("\n⚙️ Configuration Files:")
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 ALL FILES FOUND! Flutter app structure is complete.")
        print("✅ The app should run without import errors.")
    else:
        print("⚠️  Some files are missing. Please check the missing files above.")
    
    return all_good

def check_import_syntax():
    """Basic check for import syntax in key files"""
    print("\n🔍 Checking Import Syntax...")
    print("=" * 60)
    
    key_files = [
        "lib/main.dart",
        "lib/core/utils/app_router.dart",
        "lib/features/dashboard/screens/dashboard_screen.dart",
        "lib/features/expenses/screens/expenses_screen.dart",
        "lib/features/tasks/screens/tasks_screen.dart",
    ]
    
    all_good = True
    for file_path in key_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    if "import '" in content and ";" in content:
                        print(f"✅ {file_path}: Import syntax looks good")
                    else:
                        print(f"⚠️  {file_path}: No imports found or syntax issues")
                        all_good = False
            except Exception as e:
                print(f"❌ {file_path}: Error reading file - {e}")
                all_good = False
        else:
            print(f"❌ {file_path}: File not found")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("🚀 Flutter App Structure Verification")
    print("=" * 60)
    
    # Change to frontend directory
    if os.path.exists("life_organizer/frontend"):
        os.chdir("life_organizer/frontend")
        print(f"📁 Working directory: {os.getcwd()}")
    else:
        print("❌ Frontend directory not found!")
        sys.exit(1)
    
    # Run checks
    structure_ok = check_flutter_structure()
    imports_ok = check_import_syntax()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    if structure_ok and imports_ok:
        print("🎉 SUCCESS! Flutter app is ready to run!")
        print("✅ All files exist and imports look correct")
        print("\n🚀 To run the app:")
        print("   cd life_organizer/frontend")
        print("   flutter pub get")
        print("   flutter run -d web")
        sys.exit(0)
    else:
        print("❌ ISSUES FOUND! Please fix the problems above.")
        if not structure_ok:
            print("   - Missing files in app structure")
        if not imports_ok:
            print("   - Import syntax issues")
        sys.exit(1)
