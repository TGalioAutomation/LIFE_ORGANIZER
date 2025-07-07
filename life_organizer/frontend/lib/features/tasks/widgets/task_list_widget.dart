import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_theme.dart';

class TaskListWidget extends ConsumerWidget {
  const TaskListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final tasks = _getMockTasks();

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: tasks.length,
      itemBuilder: (context, index) {
        final task = tasks[index];
        return _buildTaskItem(task);
      },
    );
  }

  Widget _buildTaskItem(Map<String, dynamic> task) {
    final priority = task['priority'] as String;
    final priorityColor = _getPriorityColor(priority);
    final isCompleted = task['status'] == 'done';

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Checkbox(
          value: isCompleted,
          onChanged: (value) {
            // Handle task completion
          },
          activeColor: AppTheme.successColor,
        ),
        title: Text(
          task['title'],
          style: TextStyle(
            fontWeight: FontWeight.w500,
            decoration: isCompleted ? TextDecoration.lineThrough : null,
            color: isCompleted ? Colors.grey : null,
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (task['description'] != null) ...[
              const SizedBox(height: 4),
              Text(
                task['description'],
                style: TextStyle(
                  color: Colors.grey[600],
                  fontSize: 12,
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
                  size: 14,
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
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: priorityColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
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
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: _getStatusColor(task['status']).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _getStatusLabel(task['status']),
                    style: TextStyle(
                      color: _getStatusColor(task['status']),
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
        trailing: PopupMenuButton<String>(
          onSelected: (value) {
            switch (value) {
              case 'edit':
                // Handle edit
                break;
              case 'delete':
                // Handle delete
                break;
              case 'duplicate':
                // Handle duplicate
                break;
            }
          },
          itemBuilder: (context) => [
            const PopupMenuItem(
              value: 'edit',
              child: Row(
                children: [
                  Icon(Icons.edit, size: 16),
                  SizedBox(width: 8),
                  Text('Edit'),
                ],
              ),
            ),
            const PopupMenuItem(
              value: 'duplicate',
              child: Row(
                children: [
                  Icon(Icons.copy, size: 16),
                  SizedBox(width: 8),
                  Text('Duplicate'),
                ],
              ),
            ),
            const PopupMenuItem(
              value: 'delete',
              child: Row(
                children: [
                  Icon(Icons.delete, size: 16, color: Colors.red),
                  SizedBox(width: 8),
                  Text('Delete', style: TextStyle(color: Colors.red)),
                ],
              ),
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

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'todo':
        return AppTheme.mediumPriority;
      case 'in_progress':
        return AppTheme.primaryColor;
      case 'done':
        return AppTheme.successColor;
      default:
        return AppTheme.mediumPriority;
    }
  }

  String _getStatusLabel(String status) {
    switch (status.toLowerCase()) {
      case 'todo':
        return 'TO DO';
      case 'in_progress':
        return 'IN PROGRESS';
      case 'done':
        return 'DONE';
      default:
        return status.toUpperCase();
    }
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
      {
        'title': 'Team meeting preparation',
        'description': 'Prepare agenda and materials for weekly team meeting',
        'dueDate': 'Friday, 9:00 AM',
        'priority': 'medium',
        'status': 'todo',
      },
      {
        'title': 'Code review',
        'description': 'Review pull requests from team members',
        'dueDate': 'Today, 4:00 PM',
        'priority': 'high',
        'status': 'in_progress',
      },
    ];
  }
}
