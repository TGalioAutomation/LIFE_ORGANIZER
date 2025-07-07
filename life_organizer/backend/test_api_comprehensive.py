#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Life Organizer
Tests all major functionality and error handling
"""

import requests
import json
import sys
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.test_results = []

    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details
        })

    def test_user_registration(self):
        """Test user registration with improved error handling"""
        print("\n🔐 Testing User Registration...")
        
        # Test successful registration
        data = {
            "username": f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/auth/register/", json=data)
            if response.status_code == 201:
                result = response.json()
                self.token = result.get('access')
                self.user_id = result.get('user', {}).get('id')
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                self.log_test("User Registration", True, f"User ID: {self.user_id}")
                return True
            else:
                self.log_test("User Registration", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("User Registration", False, f"Exception: {str(e)}")
            return False

    def test_authentication(self):
        """Test login functionality"""
        print("\n🔑 Testing Authentication...")
        
        # Test login (assuming registration was successful)
        if not self.token:
            self.log_test("Authentication", False, "No token from registration")
            return False
            
        # Test token validation by accessing protected endpoint
        try:
            response = self.session.get(f"{BASE_URL}/auth/me/")
            if response.status_code == 200:
                self.log_test("Token Validation", True, "Protected endpoint accessible")
                return True
            else:
                self.log_test("Token Validation", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")
            return False

    def test_expense_management(self):
        """Test expense management functionality"""
        print("\n💰 Testing Expense Management...")
        
        # Create default categories
        try:
            response = self.session.post(f"{BASE_URL}/expenses/categories/create_defaults/")
            if response.status_code in [200, 201]:
                self.log_test("Create Default Categories", True)
            else:
                self.log_test("Create Default Categories", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Default Categories", False, f"Exception: {str(e)}")

        # Get categories
        try:
            response = self.session.get(f"{BASE_URL}/expenses/categories/")
            if response.status_code == 200:
                categories = response.json().get('results', [])
                self.log_test("Get Categories", True, f"Found {len(categories)} categories")
                
                # Create a transaction if we have categories
                if categories:
                    transaction_data = {
                        "transaction_type": "expense",
                        "amount": 25.50,
                        "description": "Test Coffee Purchase",
                        "expense_category": categories[0]['id'],
                        "transaction_date": datetime.now().isoformat()
                    }
                    
                    response = self.session.post(f"{BASE_URL}/expenses/transactions/", json=transaction_data)
                    if response.status_code == 201:
                        self.log_test("Create Transaction", True)
                    else:
                        self.log_test("Create Transaction", False, f"Status: {response.status_code}, Response: {response.text}")
            else:
                self.log_test("Get Categories", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get Categories", False, f"Exception: {str(e)}")

        # Test transaction summary
        try:
            response = self.session.get(f"{BASE_URL}/expenses/transactions/summary/")
            if response.status_code == 200:
                self.log_test("Transaction Summary", True)
            else:
                self.log_test("Transaction Summary", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Transaction Summary", False, f"Exception: {str(e)}")

    def test_task_management(self):
        """Test task management functionality"""
        print("\n📋 Testing Task Management...")
        
        # Create a workspace first
        workspace_data = {
            "name": "Test Workspace",
            "description": "Test workspace for API testing",
            "workspace_type": "personal"
        }
        
        workspace_id = None
        try:
            response = self.session.post(f"{BASE_URL}/auth/workspaces/", json=workspace_data)
            if response.status_code == 201:
                workspace_id = response.json().get('id')
                self.log_test("Create Workspace", True, f"Workspace ID: {workspace_id}")
            else:
                self.log_test("Create Workspace", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Workspace", False, f"Exception: {str(e)}")

        # Create a project
        if workspace_id:
            project_data = {
                "name": "Test Project",
                "description": "Test project for API testing",
                "workspace": workspace_id,
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).date().isoformat()
            }
            
            project_id = None
            try:
                response = self.session.post(f"{BASE_URL}/tasks/projects/", json=project_data)
                if response.status_code == 201:
                    project_id = response.json().get('id')
                    self.log_test("Create Project", True, f"Project ID: {project_id}")
                else:
                    self.log_test("Create Project", False, f"Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_test("Create Project", False, f"Exception: {str(e)}")

            # Create a task
            if project_id:
                task_data = {
                    "title": "Test Task",
                    "description": "Test task for API testing",
                    "project": project_id,
                    "workspace": workspace_id,
                    "priority": "medium",
                    "status": "todo",
                    "due_date": (datetime.now() + timedelta(days=7)).isoformat()
                }
                
                try:
                    response = self.session.post(f"{BASE_URL}/tasks/tasks/", json=task_data)
                    if response.status_code == 201:
                        self.log_test("Create Task", True)
                    else:
                        self.log_test("Create Task", False, f"Status: {response.status_code}, Response: {response.text}")
                except Exception as e:
                    self.log_test("Create Task", False, f"Exception: {str(e)}")

        # Test Kanban board
        try:
            response = self.session.get(f"{BASE_URL}/tasks/kanban/")
            if response.status_code == 200:
                self.log_test("Kanban Board", True)
            else:
                self.log_test("Kanban Board", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Kanban Board", False, f"Exception: {str(e)}")

    def test_goal_management(self):
        """Test goal management functionality"""
        print("\n🎯 Testing Goal Management...")
        
        # Create default goal categories
        try:
            response = self.session.post(f"{BASE_URL}/goals/categories/create_defaults/")
            if response.status_code in [200, 201]:
                self.log_test("Create Default Goal Categories", True)
            else:
                self.log_test("Create Default Goal Categories", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Default Goal Categories", False, f"Exception: {str(e)}")

        # Get goal categories
        try:
            response = self.session.get(f"{BASE_URL}/goals/categories/")
            if response.status_code == 200:
                categories = response.json().get('results', [])
                self.log_test("Get Goal Categories", True, f"Found {len(categories)} categories")
                
                # Create a goal if we have categories
                if categories:
                    goal_data = {
                        "title": "Test Goal",
                        "description": "Test goal for API testing",
                        "category": categories[0]['id'],
                        "goal_type": "numeric",
                        "status": "active",
                        "target_value": 100,
                        "current_value": 25,
                        "unit": "points",
                        "start_date": datetime.now().date().isoformat(),
                        "target_date": (datetime.now() + timedelta(days=90)).date().isoformat()
                    }
                    
                    response = self.session.post(f"{BASE_URL}/goals/goals/", json=goal_data)
                    if response.status_code == 201:
                        self.log_test("Create Goal", True)
                    else:
                        self.log_test("Create Goal", False, f"Status: {response.status_code}, Response: {response.text}")
            else:
                self.log_test("Get Goal Categories", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get Goal Categories", False, f"Exception: {str(e)}")

        # Test goal analytics
        try:
            response = self.session.get(f"{BASE_URL}/goals/analytics/")
            if response.status_code == 200:
                self.log_test("Goal Analytics", True)
            else:
                self.log_test("Goal Analytics", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Goal Analytics", False, f"Exception: {str(e)}")

    def test_dashboard(self):
        """Test dashboard functionality"""
        print("\n📊 Testing Dashboard...")
        
        # Test dashboard overview (this was previously broken)
        try:
            response = self.session.get(f"{BASE_URL}/dashboard/overview/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Dashboard Overview", True, f"Keys: {list(data.keys())}")
            else:
                self.log_test("Dashboard Overview", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Dashboard Overview", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive API Tests for Life Organizer")
        print("=" * 60)
        
        # Run tests in order
        if self.test_user_registration():
            self.test_authentication()
            self.test_expense_management()
            self.test_task_management()
            self.test_goal_management()
            self.test_dashboard()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['test']}: {result['details']}")
        
        return failed_tests == 0

if __name__ == "__main__":
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
