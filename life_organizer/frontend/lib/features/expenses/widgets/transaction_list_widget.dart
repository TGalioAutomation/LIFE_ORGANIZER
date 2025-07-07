import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_theme.dart';

class TransactionListWidget extends ConsumerWidget {
  const TransactionListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final transactions = _getMockTransactions();

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: transactions.length,
      itemBuilder: (context, index) {
        final transaction = transactions[index];
        return _buildTransactionItem(transaction);
      },
    );
  }

  Widget _buildTransactionItem(Map<String, dynamic> transaction) {
    final isExpense = transaction['type'] == 'expense';
    final color = isExpense ? AppTheme.expenseColor : AppTheme.incomeColor;
    final icon = isExpense ? Icons.remove_circle_outline : Icons.add_circle_outline;

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Icon(icon, color: color, size: 20),
        ),
        title: Text(
          transaction['description'],
          style: const TextStyle(fontWeight: FontWeight.w500),
        ),
        subtitle: Text(
          '${transaction['category']} • ${transaction['date']}',
          style: TextStyle(color: Colors.grey[600]),
        ),
        trailing: Text(
          '${isExpense ? '-' : '+'}\$${transaction['amount']}',
          style: TextStyle(
            color: color,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  List<Map<String, dynamic>> _getMockTransactions() {
    return [
      {
        'description': 'Coffee Shop',
        'category': 'Food & Dining',
        'amount': '4.50',
        'type': 'expense',
        'date': 'Today',
      },
      {
        'description': 'Salary',
        'category': 'Income',
        'amount': '2500.00',
        'type': 'income',
        'date': 'Yesterday',
      },
      {
        'description': 'Grocery Store',
        'category': 'Food & Dining',
        'amount': '67.89',
        'type': 'expense',
        'date': 'Yesterday',
      },
      {
        'description': 'Gas Station',
        'category': 'Transportation',
        'amount': '45.00',
        'type': 'expense',
        'date': '2 days ago',
      },
      {
        'description': 'Freelance Work',
        'category': 'Income',
        'amount': '500.00',
        'type': 'income',
        'date': '3 days ago',
      },
      {
        'description': 'Restaurant',
        'category': 'Food & Dining',
        'amount': '32.50',
        'type': 'expense',
        'date': '3 days ago',
      },
      {
        'description': 'Online Shopping',
        'category': 'Shopping',
        'amount': '89.99',
        'type': 'expense',
        'date': '4 days ago',
      },
      {
        'description': 'Movie Tickets',
        'category': 'Entertainment',
        'amount': '24.00',
        'type': 'expense',
        'date': '5 days ago',
      },
    ];
  }
}
