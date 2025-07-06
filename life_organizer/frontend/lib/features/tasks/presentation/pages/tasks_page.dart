import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/utils/app_router.dart';

class TasksPage extends StatefulWidget {
  const TasksPage({super.key});

  @override
  State<TasksPage> createState() => _TasksPageState();
}

class _TasksPageState extends State<TasksPage> with TickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tasks'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'To Do'),
            Tab(text: 'In Progress'),
            Tab(text: 'Done'),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.view_kanban),
            onPressed: () {
              // TODO: Switch to Kanban view
            },
          ),
        ],
      ),
      body: TabBarView(
        controller: _tabController,
        children: const [
          _TaskList(status: 'todo'),
          _TaskList(status: 'in_progress'),
          _TaskList(status: 'done'),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.go(AppRoutes.addTask),
        child: const Icon(Icons.add),
      ),
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}

class _TaskList extends StatelessWidget {
  final String status;
  
  const _TaskList({required this.status});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: 5,
      itemBuilder: (context, index) {
        return Card(
          child: ListTile(
            leading: Checkbox(
              value: status == 'done',
              onChanged: (value) {
                // TODO: Update task status
              },
            ),
            title: Text('Complete project proposal'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Work Project'),
                const SizedBox(height: 4),
                Row(
                  children: [
                    Icon(Icons.schedule, size: 16, color: Colors.grey),
                    const SizedBox(width: 4),
                    Text(
                      'Due tomorrow',
                      style: TextStyle(fontSize: 12, color: Colors.grey),
                    ),
                    const SizedBox(width: 16),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.red.shade100,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        'High',
                        style: TextStyle(
                          fontSize: 10,
                          color: Colors.red,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
            trailing: PopupMenuButton(
              itemBuilder: (context) => [
                const PopupMenuItem(
                  value: 'edit',
                  child: Text('Edit'),
                ),
                const PopupMenuItem(
                  value: 'delete',
                  child: Text('Delete'),
                ),
              ],
              onSelected: (value) {
                // TODO: Handle menu actions
              },
            ),
            onTap: () {
              // TODO: Show task details
            },
          ),
        );
      },
    );
  }
}
