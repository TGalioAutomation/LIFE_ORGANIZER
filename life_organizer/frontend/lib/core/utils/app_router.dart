import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/dashboard/screens/dashboard_screen.dart';
import '../../features/expenses/screens/expenses_screen.dart';
import '../../features/tasks/screens/tasks_screen.dart';

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
    initialLocation: AppRoutes.dashboard,
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

      // Main App Routes - Simplified without ShellRoute
      GoRoute(
        path: AppRoutes.dashboard,
        builder: (context, state) => MainNavigation(
          child: const DashboardScreen(),
        ),
      ),
      GoRoute(
        path: AppRoutes.expenses,
        builder: (context, state) => MainNavigation(
          child: const ExpensesScreen(),
        ),
      ),
      GoRoute(
        path: AppRoutes.tasks,
        builder: (context, state) => MainNavigation(
          child: const TasksScreen(),
        ),
      ),
      GoRoute(
        path: AppRoutes.goals,
        builder: (context, state) => MainNavigation(
          child: const GoalsPage(),
        ),
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

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: const Center(
        child: Text('Login Page - To be implemented'),
      ),
    );
  }
}

class RegisterPage extends StatelessWidget {
  const RegisterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register')),
      body: const Center(
        child: Text('Register Page - To be implemented'),
      ),
    );
  }
}

class GoalsPage extends StatelessWidget {
  const GoalsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Goals')),
      body: const Center(
        child: Text('Goals Page - To be implemented'),
      ),
    );
  }
}

class MainNavigation extends StatefulWidget {
  final Widget child;

  const MainNavigation({super.key, required this.child});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: widget.child,
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
          switch (index) {
            case 0:
              context.go(AppRoutes.dashboard);
              break;
            case 1:
              context.go(AppRoutes.expenses);
              break;
            case 2:
              context.go(AppRoutes.tasks);
              break;
            case 3:
              context.go(AppRoutes.goals);
              break;
          }
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: 'Dashboard',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_balance_wallet),
            label: 'Expenses',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.task),
            label: 'Tasks',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.flag),
            label: 'Goals',
          ),
        ],
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
            SizedBox(height: 16),
            Text('The requested page could not be found.'),
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
