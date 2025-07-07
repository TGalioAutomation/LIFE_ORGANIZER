import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_theme.dart';

class KanbanBoardWidget extends ConsumerWidget {
  const KanbanBoardWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: _buildKanbanColumn(
              'To Do',
              AppTheme.mediumPriority,
              _getTasksByStatus('todo'),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: _buildKanbanColumn(
              'In Progress',
              AppTheme.primaryColor,
              _getTasksByStatus('in_progress'),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: _buildKanbanColumn(
              'Done',
              AppTheme.successColor,
              _getTasksByStatus('done'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildKanbanColumn(String title, Color color, List<Map<String, dynamic>> tasks) {
    return Container(
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: color.withOpacity(0.2),
              borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
            ),
            child: Row(
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontWeight: FontWeight.w600,
                    color: color,
                  ),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: color,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    '${tasks.length}',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: tasks.length,
              itemBuilder: (context, index) {
                return _buildTaskCard(tasks[index]);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTaskCard(Map<String, dynamic> task) {
    final priority = task['priority'] as String;
    final priorityColor = _getPriorityColor(priority);

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    task['title'],
                    style: const TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 14,
                    ),
                  ),
                ),
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: priorityColor,
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
              ],
            ),
            if (task['description'] != null) ...[
              const SizedBox(height: 8),
              Text(
                task['description'],
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
            const SizedBox(height: 8),
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
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
                const Spacer(),
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

  List<Map<String, dynamic>> _getTasksByStatus(String status) {
    final allTasks = _getMockTasks();
    return allTasks.where((task) => task['status'] == status).toList();
  }

  List<Map<String, dynamic>> _getMockTasks() {
    return [
      {
        'title': 'Review project proposal',
        'description': 'Review the new project proposal and provide feedback',
        'dueDate': 'Today, 3:00 PM',
        'priority': 'high',
        'status': 'todo',
      },
      {
        'title': 'Call dentist for appointment',
        'description': 'Schedule routine dental checkup',
        'dueDate': 'Tomorrow, 10:00 AM',
        'priority': 'medium',
        'status': 'todo',
      },
      {
        'title': 'Update website content',
        'description': 'Update the about page with new information',
        'dueDate': 'Today, 5:00 PM',
        'priority': 'medium',
        'status': 'in_progress',
      },
      {
        'title': 'Prepare presentation',
        'description': 'Create slides for client meeting',
        'dueDate': 'Tomorrow, 2:00 PM',
        'priority': 'high',
        'status': 'in_progress',
      },
      {
        'title': 'Buy groceries',
        'description': 'Weekly grocery shopping',
        'dueDate': 'Yesterday',
        'priority': 'low',
        'status': 'done',
      },
      {
        'title': 'Submit monthly report',
        'description': 'Complete and submit the monthly progress report',
        'dueDate': 'Last week',
        'priority': 'urgent',
        'status': 'done',
      },
    ];
  }
}
