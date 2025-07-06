import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/utils/app_router.dart';

class ExpensesPage extends StatelessWidget {
  const ExpensesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Expenses'),
        actions: [
          IconButton(
            icon: const Icon(Icons.analytics),
            onPressed: () {
              // TODO: Show analytics
            },
          ),
        ],
      ),
      body: const Column(
        children: [
          _ExpenseSummaryCard(),
          Expanded(child: _ExpensesList()),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.go(AppRoutes.addExpense),
        child: const Icon(Icons.add),
      ),
    );
  }
}

class _ExpenseSummaryCard extends StatelessWidget {
  const _ExpenseSummaryCard();

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text(
              'This Month',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 8),
            const Text(
              '\$1,234.56',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.red,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Column(
                  children: [
                    const Text('Income', style: TextStyle(color: Colors.grey)),
                    Text(
                      '\$2,500',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.green,
                      ),
                    ),
                  ],
                ),
                Column(
                  children: [
                    const Text('Budget', style: TextStyle(color: Colors.grey)),
                    Text(
                      '\$1,800',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.blue,
                      ),
                    ),
                  ],
                ),
                Column(
                  children: [
                    const Text('Remaining', style: TextStyle(color: Colors.grey)),
                    Text(
                      '\$565.44',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.orange,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _ExpensesList extends StatelessWidget {
  const _ExpensesList();

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      itemCount: 10,
      itemBuilder: (context, index) {
        return Card(
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: Colors.red.shade100,
              child: Icon(Icons.shopping_cart, color: Colors.red),
            ),
            title: Text('Grocery Shopping'),
            subtitle: Text('Food & Dining • Today'),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  '-\$45.67',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.red,
                  ),
                ),
                Text(
                  '2:30 PM',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                  ),
                ),
              ],
            ),
            onTap: () {
              // TODO: Show expense details
            },
          ),
        );
      },
    );
  }
}
