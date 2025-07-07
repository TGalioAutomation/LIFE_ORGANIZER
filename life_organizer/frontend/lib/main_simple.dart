import 'package:flutter/material.dart';

void main() {
  runApp(const SimpleLifeOrganizerApp());
}

class SimpleLifeOrganizerApp extends StatelessWidget {
  const SimpleLifeOrganizerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Life Organizer',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        useMaterial3: true,
      ),
      home: const SimpleHomePage(),
    );
  }
}

class SimpleHomePage extends StatefulWidget {
  const SimpleHomePage({super.key});

  @override
  State<SimpleHomePage> createState() => _SimpleHomePageState();
}

class _SimpleHomePageState extends State<SimpleHomePage> {
  int _currentIndex = 0;

  final List<Widget> _pages = [
    const SimpleDashboard(),
    const SimpleExpenses(),
    const SimpleTasks(),
    const SimpleGoals(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Life Organizer'),
        backgroundColor: Colors.indigo,
        foregroundColor: Colors.white,
      ),
      body: _pages[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        selectedItemColor: Colors.indigo,
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

class SimpleDashboard extends StatelessWidget {
  const SimpleDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Dashboard',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 20),
          Card(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Text('Welcome to Life Organizer!'),
                  SizedBox(height: 10),
                  Text('This is a simplified version to test basic functionality.'),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class SimpleExpenses extends StatelessWidget {
  const SimpleExpenses({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Expenses',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 20),
          Card(
            child: ListTile(
              leading: Icon(Icons.remove_circle_outline, color: Colors.red),
              title: Text('Coffee Shop'),
              subtitle: Text('Food & Dining'),
              trailing: Text('-\$4.50', style: TextStyle(color: Colors.red)),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.add_circle_outline, color: Colors.green),
              title: Text('Salary'),
              subtitle: Text('Income'),
              trailing: Text('+\$2500.00', style: TextStyle(color: Colors.green)),
            ),
          ),
        ],
      ),
    );
  }
}

class SimpleTasks extends StatelessWidget {
  const SimpleTasks({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Tasks',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 20),
          Card(
            child: ListTile(
              leading: Icon(Icons.check_circle_outline, color: Colors.green),
              title: Text('Review project proposal'),
              subtitle: Text('High Priority • Due today'),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.radio_button_unchecked),
              title: Text('Call dentist'),
              subtitle: Text('Medium Priority • Due tomorrow'),
            ),
          ),
        ],
      ),
    );
  }
}

class SimpleGoals extends StatelessWidget {
  const SimpleGoals({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Goals',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 20),
          Card(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Save \$10,000', style: TextStyle(fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  LinearProgressIndicator(value: 0.3),
                  SizedBox(height: 8),
                  Text('30% Complete • \$3,000 / \$10,000'),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
