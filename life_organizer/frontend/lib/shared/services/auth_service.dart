import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client.dart';
import '../../core/storage/storage_service.dart';
import '../../core/constants/app_constants.dart';
import '../models/user_model.dart';

class AuthService {
  final Dio _apiClient;
  
  AuthService(this._apiClient);
  
  Future<AuthResponse> register({
    required String username,
    required String email,
    required String firstName,
    required String lastName,
    required String password,
    required String passwordConfirm,
  }) async {
    try {
      final response = await _apiClient.post(
        '${AppConstants.authEndpoint}/register/',
        data: {
          'username': username,
          'email': email,
          'first_name': firstName,
          'last_name': lastName,
          'password': password,
          'password_confirm': passwordConfirm,
        },
      );
      
      final authResponse = AuthResponse.fromJson(response.data);
      
      // Store tokens and user data
      await StorageService.setAuthToken(authResponse.access);
      await StorageService.setUserData(authResponse.user.toJson());
      
      return authResponse;
    } on DioException catch (e) {
      throw _handleAuthError(e);
    }
  }
  
  Future<AuthResponse> login({
    required String username,
    required String password,
  }) async {
    try {
      final response = await _apiClient.post(
        '${AppConstants.authEndpoint}/login/',
        data: {
          'username': username,
          'password': password,
        },
      );
      
      final authResponse = AuthResponse.fromJson(response.data);
      
      // Store tokens and user data
      await StorageService.setAuthToken(authResponse.access);
      await StorageService.setUserData(authResponse.user.toJson());
      
      return authResponse;
    } on DioException catch (e) {
      throw _handleAuthError(e);
    }
  }
  
  Future<void> logout() async {
    try {
      final refreshToken = await StorageService.getString('refresh_token');
      
      if (refreshToken.isNotEmpty) {
        await _apiClient.post(
          '${AppConstants.authEndpoint}/logout/',
          data: {'refresh': refreshToken},
        );
      }
    } catch (e) {
      // Continue with logout even if API call fails
    } finally {
      // Clear local storage
      await StorageService.clearAuthToken();
      await StorageService.clearUserData();
    }
  }
  
  Future<User> getCurrentUser() async {
    try {
      final response = await _apiClient.get('${AppConstants.authEndpoint}/me/');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleAuthError(e);
    }
  }
  
  Future<User> updateUser({
    String? firstName,
    String? lastName,
    String? email,
  }) async {
    try {
      final data = <String, dynamic>{};
      if (firstName != null) data['first_name'] = firstName;
      if (lastName != null) data['last_name'] = lastName;
      if (email != null) data['email'] = email;
      
      final response = await _apiClient.patch(
        '${AppConstants.authEndpoint}/me/',
        data: data,
      );
      
      final user = User.fromJson(response.data);
      await StorageService.setUserData(user.toJson());
      
      return user;
    } on DioException catch (e) {
      throw _handleAuthError(e);
    }
  }
  
  Future<void> changePassword({
    required String oldPassword,
    required String newPassword,
    required String newPasswordConfirm,
  }) async {
    try {
      await _apiClient.post(
        '${AppConstants.authEndpoint}/change-password/',
        data: {
          'old_password': oldPassword,
          'new_password': newPassword,
          'new_password_confirm': newPasswordConfirm,
        },
      );
    } on DioException catch (e) {
      throw _handleAuthError(e);
    }
  }
  
  Future<bool> isLoggedIn() async {
    final token = await StorageService.getAuthToken();
    return token != null && token.isNotEmpty;
  }
  
  Future<User?> getCachedUser() async {
    final userData = await StorageService.getUserData();
    if (userData != null) {
      return User.fromJson(userData);
    }
    return null;
  }
  
  String _handleAuthError(DioException e) {
    if (e.response?.statusCode == 400) {
      final errors = e.response?.data;
      if (errors is Map<String, dynamic>) {
        // Return first error message
        for (final value in errors.values) {
          if (value is List && value.isNotEmpty) {
            return value.first.toString();
          }
        }
      }
      return 'Invalid input data';
    } else if (e.response?.statusCode == 401) {
      return 'Invalid credentials';
    } else if (e.response?.statusCode == 404) {
      return 'User not found';
    } else {
      return 'Network error. Please try again.';
    }
  }
}

// Provider for AuthService
final authServiceProvider = Provider<AuthService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return AuthService(apiClient);
});

// Auth state provider
final authStateProvider = StateNotifierProvider<AuthStateNotifier, AuthState>((ref) {
  final authService = ref.watch(authServiceProvider);
  return AuthStateNotifier(authService);
});

class AuthStateNotifier extends StateNotifier<AuthState> {
  final AuthService _authService;
  
  AuthStateNotifier(this._authService) : super(AuthState.initial()) {
    _checkAuthStatus();
  }
  
  Future<void> _checkAuthStatus() async {
    state = state.copyWith(isLoading: true);
    
    try {
      final isLoggedIn = await _authService.isLoggedIn();
      if (isLoggedIn) {
        final user = await _authService.getCachedUser();
        if (user != null) {
          state = AuthState.authenticated(user);
        } else {
          // Try to fetch user from API
          final currentUser = await _authService.getCurrentUser();
          state = AuthState.authenticated(currentUser);
        }
      } else {
        state = AuthState.unauthenticated();
      }
    } catch (e) {
      state = AuthState.unauthenticated();
    }
  }
  
  Future<void> login(String username, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      final authResponse = await _authService.login(
        username: username,
        password: password,
      );
      state = AuthState.authenticated(authResponse.user);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }
  
  Future<void> register({
    required String username,
    required String email,
    required String firstName,
    required String lastName,
    required String password,
    required String passwordConfirm,
  }) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      final authResponse = await _authService.register(
        username: username,
        email: email,
        firstName: firstName,
        lastName: lastName,
        password: password,
        passwordConfirm: passwordConfirm,
      );
      state = AuthState.authenticated(authResponse.user);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }
  
  Future<void> logout() async {
    await _authService.logout();
    state = AuthState.unauthenticated();
  }
  
  void clearError() {
    state = state.copyWith(error: null);
  }
}

class AuthState {
  final bool isAuthenticated;
  final bool isLoading;
  final User? user;
  final String? error;
  
  const AuthState({
    required this.isAuthenticated,
    required this.isLoading,
    this.user,
    this.error,
  });
  
  factory AuthState.initial() {
    return const AuthState(
      isAuthenticated: false,
      isLoading: true,
    );
  }
  
  factory AuthState.authenticated(User user) {
    return AuthState(
      isAuthenticated: true,
      isLoading: false,
      user: user,
    );
  }
  
  factory AuthState.unauthenticated() {
    return const AuthState(
      isAuthenticated: false,
      isLoading: false,
    );
  }
  
  AuthState copyWith({
    bool? isAuthenticated,
    bool? isLoading,
    User? user,
    String? error,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      isLoading: isLoading ?? this.isLoading,
      user: user ?? this.user,
      error: error,
    );
  }
}
