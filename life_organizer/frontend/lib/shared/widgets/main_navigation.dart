import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../core/utils/app_router.dart';

class MainNavigation extends StatelessWidget {
  final Widget child;
  
  const MainNavigation({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: child,
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _getCurrentIndex(context),
        onTap: (index) => _onItemTapped(context, index),
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
            icon: Icon(Icons.task_alt),
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
  
  int _getCurrentIndex(BuildContext context) {
    final location = GoRouterState.of(context).uri.path;
    
    if (location.startsWith('/dashboard')) return 0;
    if (location.startsWith('/expenses')) return 1;
    if (location.startsWith('/tasks')) return 2;
    if (location.startsWith('/goals')) return 3;
    
    return 0;
  }
  
  void _onItemTapped(BuildContext context, int index) {
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
  }
}
