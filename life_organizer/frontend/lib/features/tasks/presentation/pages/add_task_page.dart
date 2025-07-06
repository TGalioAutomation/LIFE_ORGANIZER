import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AddTaskPage extends StatefulWidget {
  const AddTaskPage({super.key});

  @override
  State<AddTaskPage> createState() => _AddTaskPageState();
}

class _AddTaskPageState extends State<AddTaskPage> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  String _selectedPriority = 'Medium';
  String _selectedProject = 'Personal';
  DateTime? _dueDate;

  final List<String> _priorities = ['Low', 'Medium', 'High', 'Urgent'];
  final List<String> _projects = ['Personal', 'Work', 'Home', 'Health'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Task'),
        actions: [
          TextButton(
            onPressed: _saveTask,
            child: const Text('Save'),
          ),
        ],
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            TextFormField(
              controller: _titleController,
              decoration: const InputDecoration(
                labelText: 'Task Title',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter a task title';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _descriptionController,
              decoration: const InputDecoration(
                labelText: 'Description',
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _selectedProject,
              decoration: const InputDecoration(
                labelText: 'Project',
              ),
              items: _projects.map((project) {
                return DropdownMenuItem(
                  value: project,
                  child: Text(project),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedProject = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _selectedPriority,
              decoration: const InputDecoration(
                labelText: 'Priority',
              ),
              items: _priorities.map((priority) {
                return DropdownMenuItem(
                  value: priority,
                  child: Row(
                    children: [
                      Container(
                        width: 12,
                        height: 12,
                        decoration: BoxDecoration(
                          color: _getPriorityColor(priority),
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(priority),
                    ],
                  ),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedPriority = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            ListTile(
              title: const Text('Due Date'),
              subtitle: Text(
                _dueDate != null
                    ? '${_dueDate!.day}/${_dueDate!.month}/${_dueDate!.year}'
                    : 'No due date',
              ),
              trailing: const Icon(Icons.calendar_today),
              onTap: _selectDueDate,
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      // TODO: Add subtasks
                    },
                    icon: const Icon(Icons.list),
                    label: const Text('Add Subtasks'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      // TODO: Set reminder
                    },
                    icon: const Icon(Icons.notifications),
                    label: const Text('Set Reminder'),
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
    switch (priority) {
      case 'Low':
        return Colors.green;
      case 'Medium':
        return Colors.orange;
      case 'High':
        return Colors.red;
      case 'Urgent':
        return Colors.purple;
      default:
        return Colors.grey;
    }
  }

  Future<void> _selectDueDate() async {
    final date = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    
    if (date != null) {
      setState(() {
        _dueDate = date;
      });
    }
  }

  void _saveTask() {
    if (_formKey.currentState!.validate()) {
      // TODO: Save task
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Task saved successfully')),
      );
      context.pop();
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }
}
