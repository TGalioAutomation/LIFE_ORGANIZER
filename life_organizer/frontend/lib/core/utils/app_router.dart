import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/auth/presentation/pages/register_page.dart';
import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/expenses/presentation/pages/expenses_page.dart';
import '../../features/expenses/presentation/pages/add_expense_page.dart';
import '../../features/tasks/presentation/pages/tasks_page.dart';
import '../../features/tasks/presentation/pages/add_task_page.dart';
import '../../features/goals/presentation/pages/goals_page.dart';
import '../../features/goals/presentation/pages/add_goal_page.dart';
import '../../shared/widgets/main_navigation.dart';

// Route names
class AppRoutes {
  static const String splash = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String dashboard = '/dashboard';
  static const String expenses = '/expenses';
  static const String addExpense = '/expenses/add';
  static const String tasks = '/tasks';
  static const String addTask = '/tasks/add';
  static const String goals = '/goals';
  static const String addGoal = '/goals/add';
  static const String profile = '/profile';
  static const String settings = '/settings';
}

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: AppRoutes.splash,
    routes: [
      // Splash/Auth Routes
      GoRoute(
        path: AppRoutes.splash,
        builder: (context, state) => const SplashPage(),
      ),
      GoRoute(
        path: AppRoutes.login,
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: AppRoutes.register,
        builder: (context, state) => const RegisterPage(),
      ),
      
      // Main App Routes with Bottom Navigation
      ShellRoute(
        builder: (context, state, child) => MainNavigation(child: child),
        routes: [
          GoRoute(
            path: AppRoutes.dashboard,
            builder: (context, state) => const DashboardPage(),
          ),
          GoRoute(
            path: AppRoutes.expenses,
            builder: (context, state) => const ExpensesPage(),
            routes: [
              GoRoute(
                path: '/add',
                builder: (context, state) => const AddExpensePage(),
              ),
            ],
          ),
          GoRoute(
            path: AppRoutes.tasks,
            builder: (context, state) => const TasksPage(),
            routes: [
              GoRoute(
                path: '/add',
                builder: (context, state) => const AddTaskPage(),
              ),
            ],
          ),
          GoRoute(
            path: AppRoutes.goals,
            builder: (context, state) => const GoalsPage(),
            routes: [
              GoRoute(
                path: '/add',
                builder: (context, state) => const AddGoalPage(),
              ),
            ],
          ),
        ],
      ),
    ],
    errorBuilder: (context, state) => const ErrorPage(),
  );
});

// Placeholder pages - will be implemented later
class SplashPage extends StatelessWidget {
  const SplashPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.apps, size: 64),
            SizedBox(height: 16),
            Text('Life Organizer', style: TextStyle(fontSize: 24)),
            SizedBox(height: 16),
            CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}

class ErrorPage extends StatelessWidget {
  const ErrorPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Error')),
      body: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.error_outline, size: 64, color: Colors.red),
            SizedBox(height: 16),
            Text('Page not found', style: TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
