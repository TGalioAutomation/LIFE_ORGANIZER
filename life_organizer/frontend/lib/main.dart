import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/theme/app_theme.dart';
import 'core/constants/app_constants.dart';
import 'core/utils/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize services with error handling
  try {
    // Note: Services initialization commented out for initial testing
    // await Hive.initFlutter();
    // await StorageService.init();
    // ApiClient.init();
  } catch (e) {
    print('Service initialization error: $e');
  }

  runApp(
    const ProviderScope(
      child: LifeOrganizerApp(),
    ),
  );
}

class LifeOrganizerApp extends ConsumerWidget {
  const LifeOrganizerApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    try {
      final router = ref.watch(routerProvider);

      return MaterialApp.router(
        title: AppConstants.appName,
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.system,
        routerConfig: router,
      );
    } catch (e) {
      print('Router error: $e');
      // Fallback to simple MaterialApp
      return MaterialApp(
        title: AppConstants.appName,
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.system,
        home: Scaffold(
          appBar: AppBar(title: const Text('Life Organizer')),
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 64, color: Colors.red),
                const SizedBox(height: 16),
                const Text('Router Error'),
                const SizedBox(height: 8),
                Text('Error: $e'),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {
                    // Try to restart the app
                  },
                  child: const Text('Retry'),
                ),
              ],
            ),
          ),
        ),
      );
    }
  }
}
