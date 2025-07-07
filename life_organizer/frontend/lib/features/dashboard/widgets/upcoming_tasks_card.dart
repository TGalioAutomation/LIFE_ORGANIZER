import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_theme.dart';

class UpcomingTasksCard extends ConsumerWidget {
  const UpcomingTasksCard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final tasks = _getMockTasks();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(
                  'Upcoming Tasks',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const Spacer(),
                TextButton(
                  onPressed: () {
                    // Navigate to all tasks
                  },
                  child: const Text('View All'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ...tasks.map((task) => _buildTaskItem(task)),
          ],
        ),
      ),
    );
  }

  Widget _buildTaskItem(Map<String, dynamic> task) {
    final priority = task['priority'] as String;
    final priorityColor = _getPriorityColor(priority);

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Container(
            width: 4,
            height: 40,
            decoration: BoxDecoration(
              color: priorityColor,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  task['title'],
                  style: const TextStyle(
                    fontWeight: FontWeight.w500,
                    fontSize: 14,
                  ),
                ),
                const SizedBox(height: 2),
                Row(
                  children: [
                    Icon(
                      Icons.schedule,
                      size: 12,
                      color: Colors.grey[600],
                    ),
                    const SizedBox(width: 4),
                    Text(
                      task['dueDate'],
                      style: TextStyle(
                        color: Colors.grey[600],
                        fontSize: 12,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: priorityColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        priority.toUpperCase(),
                        style: TextStyle(
                          color: priorityColor,
                          fontSize: 10,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.check_circle_outline),
            onPressed: () {
              // Mark task as complete
            },
            iconSize: 20,
            color: AppTheme.secondaryColor,
          ),
        ],
      ),
    );
  }

  Color _getPriorityColor(String priority) {
    switch (priority.toLowerCase()) {
      case 'high':
        return AppTheme.highPriority;
      case 'medium':
        return AppTheme.mediumPriority;
      case 'low':
        return AppTheme.lowPriority;
      case 'urgent':
        return AppTheme.urgentPriority;
      default:
        return AppTheme.mediumPriority;
    }
  }

  List<Map<String, dynamic>> _getMockTasks() {
    return [
      {
        'title': 'Review project proposal',
        'dueDate': 'Today, 3:00 PM',
        'priority': 'high',
      },
      {
        'title': 'Call dentist for appointment',
        'dueDate': 'Tomorrow, 10:00 AM',
        'priority': 'medium',
      },
      {
        'title': 'Buy groceries',
        'dueDate': 'Tomorrow, 6:00 PM',
        'priority': 'low',
      },
      {
        'title': 'Submit monthly report',
        'dueDate': 'Friday, 5:00 PM',
        'priority': 'urgent',
      },
    ];
  }
}
