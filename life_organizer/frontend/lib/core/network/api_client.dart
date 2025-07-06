import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';

import '../constants/app_constants.dart';
import '../storage/storage_service.dart';
import 'api_interceptor.dart';

class ApiClient {
  static late Dio _dio;
  static final Logger _logger = Logger();
  
  static void init() {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConstants.baseUrl,
        connectTimeout: AppConstants.connectionTimeout,
        receiveTimeout: AppConstants.apiTimeout,
        sendTimeout: AppConstants.apiTimeout,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );
    
    // Add interceptors
    _dio.interceptors.add(ApiInterceptor());
    
    // Add logging interceptor in debug mode
    _dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
        logPrint: (object) => _logger.d(object),
      ),
    );
  }
  
  static Dio get instance => _dio;
  
  // GET request
  static Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      _logger.e('GET request failed: ${e.message}');
      rethrow;
    }
  }
  
  // POST request
  static Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      _logger.e('POST request failed: ${e.message}');
      rethrow;
    }
  }
  
  // PUT request
  static Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.put<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      _logger.e('PUT request failed: ${e.message}');
      rethrow;
    }
  }
  
  // PATCH request
  static Future<Response<T>> patch<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.patch<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      _logger.e('PATCH request failed: ${e.message}');
      rethrow;
    }
  }
  
  // DELETE request
  static Future<Response<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.delete<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      _logger.e('DELETE request failed: ${e.message}');
      rethrow;
    }
  }
  
  // Upload file
  static Future<Response<T>> uploadFile<T>(
    String path,
    String filePath, {
    Map<String, dynamic>? data,
    ProgressCallback? onSendProgress,
  }) async {
    try {
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(filePath),
        ...?data,
      });
      
      return await _dio.post<T>(
        path,
        data: formData,
        onSendProgress: onSendProgress,
      );
    } on DioException catch (e) {
      _logger.e('File upload failed: ${e.message}');
      rethrow;
    }
  }
}

// Provider for API client
final apiClientProvider = Provider<Dio>((ref) {
  return ApiClient.instance;
});
