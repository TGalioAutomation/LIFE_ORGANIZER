import 'package:flutter/material.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () {
              // TODO: Show notifications
            },
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              // TODO: Navigate to settings
            },
          ),
        ],
      ),
      body: const SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome back!',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 16),
            _QuickStatsSection(),
            SizedBox(height: 24),
            _RecentActivitySection(),
            SizedBox(height: 24),
            _UpcomingTasksSection(),
          ],
        ),
      ),
    );
  }
}

class _QuickStatsSection extends StatelessWidget {
  const _QuickStatsSection();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Quick Stats',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _StatCard(
                title: 'This Month',
                value: '\$1,234',
                subtitle: 'Expenses',
                color: Colors.red,
                icon: Icons.trending_down,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _StatCard(
                title: 'Pending',
                value: '8',
                subtitle: 'Tasks',
                color: Colors.orange,
                icon: Icons.task_alt,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _StatCard(
                title: 'Active',
                value: '5',
                subtitle: 'Goals',
                color: Colors.blue,
                icon: Icons.flag,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _StatCard(
                title: 'Budget',
                value: '75%',
                subtitle: 'Used',
                color: Colors.green,
                icon: Icons.account_balance_wallet,
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  final String subtitle;
  final Color color;
  final IconData icon;

  const _StatCard({
    required this.title,
    required this.value,
    required this.subtitle,
    required this.color,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 20),
                const SizedBox(width: 8),
                Text(title, style: const TextStyle(fontSize: 12)),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            Text(
              subtitle,
              style: const TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}

class _RecentActivitySection extends StatelessWidget {
  const _RecentActivitySection();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Recent Activity',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        Card(
          child: ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: 3,
            separatorBuilder: (context, index) => const Divider(),
            itemBuilder: (context, index) {
              return ListTile(
                leading: const CircleAvatar(
                  child: Icon(Icons.shopping_cart),
                ),
                title: Text('Grocery Shopping'),
                subtitle: Text('2 hours ago'),
                trailing: Text('-\$45.67'),
              );
            },
          ),
        ),
      ],
    );
  }
}

class _UpcomingTasksSection extends StatelessWidget {
  const _UpcomingTasksSection();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Upcoming Tasks',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        Card(
          child: ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: 3,
            separatorBuilder: (context, index) => const Divider(),
            itemBuilder: (context, index) {
              return ListTile(
                leading: Checkbox(
                  value: false,
                  onChanged: (value) {},
                ),
                title: Text('Complete project proposal'),
                subtitle: Text('Due tomorrow'),
                trailing: const Icon(Icons.priority_high, color: Colors.red),
              );
            },
          ),
        ),
      ],
    );
  }
}
