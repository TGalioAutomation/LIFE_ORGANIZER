import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AddGoalPage extends StatefulWidget {
  const AddGoalPage({super.key});

  @override
  State<AddGoalPage> createState() => _AddGoalPageState();
}

class _AddGoalPageState extends State<AddGoalPage> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _targetValueController = TextEditingController();
  String _selectedType = 'Numeric Target';
  String _selectedCategory = 'Personal Development';
  String _selectedFrequency = 'One Time';
  DateTime _targetDate = DateTime.now().add(const Duration(days: 30));

  final List<String> _goalTypes = [
    'Numeric Target',
    'Yes/No Achievement',
    'Daily/Weekly Habit',
    'Financial Target',
  ];

  final List<String> _categories = [
    'Personal Development',
    'Health & Fitness',
    'Career',
    'Financial',
    'Relationships',
    'Hobbies',
    'Education',
    'Travel',
  ];

  final List<String> _frequencies = [
    'Daily',
    'Weekly',
    'Monthly',
    'Yearly',
    'One Time',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Goal'),
        actions: [
          TextButton(
            onPressed: _saveGoal,
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
                labelText: 'Goal Title',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter a goal title';
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
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter a description';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _selectedType,
              decoration: const InputDecoration(
                labelText: 'Goal Type',
              ),
              items: _goalTypes.map((type) {
                return DropdownMenuItem(
                  value: type,
                  child: Text(type),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedType = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _selectedCategory,
              decoration: const InputDecoration(
                labelText: 'Category',
              ),
              items: _categories.map((category) {
                return DropdownMenuItem(
                  value: category,
                  child: Text(category),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedCategory = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            if (_selectedType == 'Numeric Target' || _selectedType == 'Financial Target')
              TextFormField(
                controller: _targetValueController,
                decoration: InputDecoration(
                  labelText: _selectedType == 'Financial Target' ? 'Target Amount' : 'Target Value',
                  prefixText: _selectedType == 'Financial Target' ? '\$' : '',
                ),
                keyboardType: TextInputType.numberWithOptions(decimal: true),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a target value';
                  }
                  if (double.tryParse(value) == null) {
                    return 'Please enter a valid number';
                  }
                  return null;
                },
              ),
            if (_selectedType == 'Numeric Target' || _selectedType == 'Financial Target')
              const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _selectedFrequency,
              decoration: const InputDecoration(
                labelText: 'Frequency',
              ),
              items: _frequencies.map((frequency) {
                return DropdownMenuItem(
                  value: frequency,
                  child: Text(frequency),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedFrequency = value!;
                });
              },
            ),
            const SizedBox(height: 16),
            ListTile(
              title: const Text('Target Date'),
              subtitle: Text(
                '${_targetDate.day}/${_targetDate.month}/${_targetDate.year}',
              ),
              trailing: const Icon(Icons.calendar_today),
              onTap: _selectTargetDate,
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      // TODO: Add milestones
                    },
                    icon: const Icon(Icons.flag),
                    label: const Text('Add Milestones'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      // TODO: Set reminders
                    },
                    icon: const Icon(Icons.notifications),
                    label: const Text('Set Reminders'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _selectTargetDate() async {
    final date = await showDatePicker(
      context: context,
      initialDate: _targetDate,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365 * 5)),
    );
    
    if (date != null) {
      setState(() {
        _targetDate = date;
      });
    }
  }

  void _saveGoal() {
    if (_formKey.currentState!.validate()) {
      // TODO: Save goal
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Goal saved successfully')),
      );
      context.pop();
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    _targetValueController.dispose();
    super.dispose();
  }
}
