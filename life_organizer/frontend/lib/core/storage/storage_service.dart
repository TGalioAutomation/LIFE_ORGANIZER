import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../constants/app_constants.dart';

class StorageService {
  static late SharedPreferences _prefs;
  static const FlutterSecureStorage _secureStorage = FlutterSecureStorage();
  static late Box _hiveBox;
  
  static Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
    _hiveBox = await Hive.openBox('app_data');
  }
  
  // Secure Storage (for sensitive data like tokens)
  static Future<void> setAuthToken(String token) async {
    await _secureStorage.write(key: AppConstants.authTokenKey, value: token);
  }
  
  static Future<String?> getAuthToken() async {
    return await _secureStorage.read(key: AppConstants.authTokenKey);
  }
  
  static Future<void> clearAuthToken() async {
    await _secureStorage.delete(key: AppConstants.authTokenKey);
  }
  
  // User Data
  static Future<void> setUserData(Map<String, dynamic> userData) async {
    await _secureStorage.write(
      key: AppConstants.userDataKey,
      value: jsonEncode(userData),
    );
  }
  
  static Future<Map<String, dynamic>?> getUserData() async {
    final userData = await _secureStorage.read(key: AppConstants.userDataKey);
    if (userData != null) {
      return jsonDecode(userData) as Map<String, dynamic>;
    }
    return null;
  }
  
  static Future<void> clearUserData() async {
    await _secureStorage.delete(key: AppConstants.userDataKey);
  }
  
  // Preferences (non-sensitive data)
  static Future<void> setThemePreference(String theme) async {
    await _prefs.setString(AppConstants.themeKey, theme);
  }
  
  static String getThemePreference() {
    return _prefs.getString(AppConstants.themeKey) ?? 'system';
  }
  
  static Future<void> setLanguagePreference(String language) async {
    await _prefs.setString(AppConstants.languageKey, language);
  }
  
  static String getLanguagePreference() {
    return _prefs.getString(AppConstants.languageKey) ?? 'en';
  }
  
  // Generic preference methods
  static Future<void> setBool(String key, bool value) async {
    await _prefs.setBool(key, value);
  }
  
  static bool getBool(String key, {bool defaultValue = false}) {
    return _prefs.getBool(key) ?? defaultValue;
  }
  
  static Future<void> setString(String key, String value) async {
    await _prefs.setString(key, value);
  }
  
  static String getString(String key, {String defaultValue = ''}) {
    return _prefs.getString(key) ?? defaultValue;
  }
  
  static Future<void> setInt(String key, int value) async {
    await _prefs.setInt(key, value);
  }
  
  static int getInt(String key, {int defaultValue = 0}) {
    return _prefs.getInt(key) ?? defaultValue;
  }
  
  static Future<void> setDouble(String key, double value) async {
    await _prefs.setDouble(key, value);
  }
  
  static double getDouble(String key, {double defaultValue = 0.0}) {
    return _prefs.getDouble(key) ?? defaultValue;
  }
  
  // Hive Storage (for complex objects and offline data)
  static Future<void> putHiveData(String key, dynamic value) async {
    await _hiveBox.put(key, value);
  }
  
  static T? getHiveData<T>(String key) {
    return _hiveBox.get(key) as T?;
  }
  
  static Future<void> deleteHiveData(String key) async {
    await _hiveBox.delete(key);
  }
  
  static Future<void> clearHiveData() async {
    await _hiveBox.clear();
  }
  
  // Cache management
  static Future<void> cacheExpenseData(List<Map<String, dynamic>> expenses) async {
    await putHiveData('cached_expenses', expenses);
    await putHiveData('expenses_cache_time', DateTime.now().millisecondsSinceEpoch);
  }
  
  static List<Map<String, dynamic>>? getCachedExpenseData() {
    final cacheTime = getHiveData<int>('expenses_cache_time');
    if (cacheTime != null) {
      final cacheAge = DateTime.now().millisecondsSinceEpoch - cacheTime;
      // Cache valid for 5 minutes
      if (cacheAge < 5 * 60 * 1000) {
        return getHiveData<List<Map<String, dynamic>>>('cached_expenses');
      }
    }
    return null;
  }
  
  static Future<void> cacheTaskData(List<Map<String, dynamic>> tasks) async {
    await putHiveData('cached_tasks', tasks);
    await putHiveData('tasks_cache_time', DateTime.now().millisecondsSinceEpoch);
  }
  
  static List<Map<String, dynamic>>? getCachedTaskData() {
    final cacheTime = getHiveData<int>('tasks_cache_time');
    if (cacheTime != null) {
      final cacheAge = DateTime.now().millisecondsSinceEpoch - cacheTime;
      // Cache valid for 5 minutes
      if (cacheAge < 5 * 60 * 1000) {
        return getHiveData<List<Map<String, dynamic>>>('cached_tasks');
      }
    }
    return null;
  }
  
  // Clear all data
  static Future<void> clearAllData() async {
    await _secureStorage.deleteAll();
    await _prefs.clear();
    await _hiveBox.clear();
  }
}
