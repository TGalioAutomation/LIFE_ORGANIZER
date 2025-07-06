import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/network/api_client.dart';
import '../../core/constants/app_constants.dart';
import '../models/expense_model.dart';

class ExpenseService {
  final Dio _apiClient;
  
  ExpenseService(this._apiClient);
  
  // Expense Categories
  Future<List<ExpenseCategory>> getExpenseCategories() async {
    try {
      final response = await _apiClient.get('${AppConstants.expensesEndpoint}/categories/');
      final List<dynamic> data = response.data['results'] ?? response.data;
      return data.map((json) => ExpenseCategory.fromJson(json)).toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<List<ExpenseCategory>> createDefaultExpenseCategories() async {
    try {
      final response = await _apiClient.post('${AppConstants.expensesEndpoint}/categories/create_defaults/');
      final List<dynamic> data = response.data['categories'];
      return data.map((json) => ExpenseCategory.fromJson(json)).toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<ExpenseCategory> createExpenseCategory({
    required String name,
    String? description,
    String? icon,
    String? color,
  }) async {
    try {
      final response = await _apiClient.post(
        '${AppConstants.expensesEndpoint}/categories/',
        data: {
          'name': name,
          'description': description ?? '',
          'icon': icon ?? '',
          'color': color ?? '#007bff',
        },
      );
      return ExpenseCategory.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Income Categories
  Future<List<IncomeCategory>> getIncomeCategories() async {
    try {
      final response = await _apiClient.get('${AppConstants.expensesEndpoint}/income-categories/');
      final List<dynamic> data = response.data['results'] ?? response.data;
      return data.map((json) => IncomeCategory.fromJson(json)).toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<List<IncomeCategory>> createDefaultIncomeCategories() async {
    try {
      final response = await _apiClient.post('${AppConstants.expensesEndpoint}/income-categories/create_defaults/');
      final List<dynamic> data = response.data['categories'];
      return data.map((json) => IncomeCategory.fromJson(json)).toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Transactions
  Future<List<Transaction>> getTransactions({
    int page = 1,
    int pageSize = 20,
    TransactionType? type,
    String? startDate,
    String? endDate,
    String? search,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
      };
      
      if (type != null) {
        queryParams['transaction_type'] = type == TransactionType.income ? 'income' : 'expense';
      }
      if (startDate != null) queryParams['start_date'] = startDate;
      if (endDate != null) queryParams['end_date'] = endDate;
      if (search != null && search.isNotEmpty) queryParams['search'] = search;
      
      final response = await _apiClient.get(
        '${AppConstants.expensesEndpoint}/transactions/',
        queryParameters: queryParams,
      );
      
      final List<dynamic> data = response.data['results'] ?? response.data;
      return data.map((json) => Transaction.fromJson(json)).toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<List<Transaction>> getRecentTransactions() async {
    try {
      final response = await _apiClient.get('${AppConstants.expensesEndpoint}/transactions/recent/');
      final List<dynamic> data = response.data;
      return data.map((json) => Transaction.fromJson(json)).toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Transaction> createTransaction({
    required TransactionType type,
    required double amount,
    required String description,
    String? notes,
    int? expenseCategoryId,
    int? incomeCategoryId,
    DateTime? transactionDate,
    String? location,
    bool voiceInput = false,
  }) async {
    try {
      final data = {
        'transaction_type': type == TransactionType.income ? 'income' : 'expense',
        'amount': amount,
        'description': description,
        'notes': notes ?? '',
        'transaction_date': (transactionDate ?? DateTime.now()).toIso8601String(),
        'location': location ?? '',
        'voice_input': voiceInput,
      };
      
      if (type == TransactionType.expense && expenseCategoryId != null) {
        data['expense_category'] = expenseCategoryId;
      } else if (type == TransactionType.income && incomeCategoryId != null) {
        data['income_category'] = incomeCategoryId;
      }
      
      final response = await _apiClient.post(
        '${AppConstants.expensesEndpoint}/transactions/',
        data: data,
      );
      
      return Transaction.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Transaction> updateTransaction({
    required int id,
    TransactionType? type,
    double? amount,
    String? description,
    String? notes,
    int? expenseCategoryId,
    int? incomeCategoryId,
    DateTime? transactionDate,
    String? location,
  }) async {
    try {
      final data = <String, dynamic>{};
      
      if (type != null) {
        data['transaction_type'] = type == TransactionType.income ? 'income' : 'expense';
      }
      if (amount != null) data['amount'] = amount;
      if (description != null) data['description'] = description;
      if (notes != null) data['notes'] = notes;
      if (transactionDate != null) data['transaction_date'] = transactionDate.toIso8601String();
      if (location != null) data['location'] = location;
      if (expenseCategoryId != null) data['expense_category'] = expenseCategoryId;
      if (incomeCategoryId != null) data['income_category'] = incomeCategoryId;
      
      final response = await _apiClient.patch(
        '${AppConstants.expensesEndpoint}/transactions/$id/',
        data: data,
      );
      
      return Transaction.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<void> deleteTransaction(int id) async {
    try {
      await _apiClient.delete('${AppConstants.expensesEndpoint}/transactions/$id/');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Analytics
  Future<TransactionSummary> getTransactionSummary({
    String? startDate,
    String? endDate,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (startDate != null) queryParams['start_date'] = startDate;
      if (endDate != null) queryParams['end_date'] = endDate;
      
      final response = await _apiClient.get(
        '${AppConstants.expensesEndpoint}/transactions/summary/',
        queryParameters: queryParams,
      );
      
      return TransactionSummary.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> getExpenseAnalytics({
    String? startDate,
    String? endDate,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (startDate != null) queryParams['start_date'] = startDate;
      if (endDate != null) queryParams['end_date'] = endDate;
      
      final response = await _apiClient.get(
        '${AppConstants.expensesEndpoint}/analytics/',
        queryParameters: queryParams,
      );
      
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> getMonthlySummary({
    int? month,
    int? year,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (month != null) queryParams['month'] = month;
      if (year != null) queryParams['year'] = year;
      
      final response = await _apiClient.get(
        '${AppConstants.expensesEndpoint}/monthly-summary/',
        queryParameters: queryParams,
      );
      
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  String _handleError(DioException e) {
    if (e.response?.statusCode == 400) {
      return 'Invalid data provided';
    } else if (e.response?.statusCode == 401) {
      return 'Authentication required';
    } else if (e.response?.statusCode == 403) {
      return 'Access denied';
    } else if (e.response?.statusCode == 404) {
      return 'Resource not found';
    } else {
      return 'Network error. Please try again.';
    }
  }
}

// Provider for ExpenseService
final expenseServiceProvider = Provider<ExpenseService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return ExpenseService(apiClient);
});
