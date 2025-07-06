import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/theme/app_theme.dart';
import 'core/constants/app_constants.dart';
import 'core/network/api_client.dart';
import 'core/storage/storage_service.dart';
import 'core/utils/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive for local storage
  await Hive.initFlutter();
  
  // Initialize storage service
  await StorageService.init();
  
  // Initialize API client
  ApiClient.init();
  
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
    final router = ref.watch(routerProvider);
    
    return MaterialApp.router(
      title: AppConstants.appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routerConfig: router,
    );
  }
}
