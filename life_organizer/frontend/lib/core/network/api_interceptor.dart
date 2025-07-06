import 'package:dio/dio.dart';
import 'package:logger/logger.dart';

import '../constants/app_constants.dart';
import '../storage/storage_service.dart';

class ApiInterceptor extends Interceptor {
  final Logger _logger = Logger();
  
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // Add authentication token if available
    final token = await StorageService.getAuthToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    
    _logger.d('Request: ${options.method} ${options.uri}');
    _logger.d('Headers: ${options.headers}');
    
    super.onRequest(options, handler);
  }
  
  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    _logger.d('Response: ${response.statusCode} ${response.requestOptions.uri}');
    super.onResponse(response, handler);
  }
  
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    _logger.e('Error: ${err.response?.statusCode} ${err.requestOptions.uri}');
    _logger.e('Error message: ${err.message}');
    
    // Handle token expiration
    if (err.response?.statusCode == 401) {
      await _handleUnauthorized();
    }
    
    super.onError(err, handler);
  }
  
  Future<void> _handleUnauthorized() async {
    // Clear stored authentication data
    await StorageService.clearAuthToken();
    await StorageService.clearUserData();
    
    // Navigate to login screen
    // This would typically be handled by a navigation service
    _logger.w('User session expired, redirecting to login');
  }
}
