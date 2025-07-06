class User {
  final int id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final DateTime dateJoined;
  
  const User({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.dateJoined,
  });
  
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      username: json['username'] as String,
      email: json['email'] as String,
      firstName: json['first_name'] as String? ?? '',
      lastName: json['last_name'] as String? ?? '',
      dateJoined: DateTime.parse(json['date_joined'] as String),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'date_joined': dateJoined.toIso8601String(),
    };
  }
  
  String get fullName {
    return '$firstName $lastName'.trim();
  }
  
  String get initials {
    final first = firstName.isNotEmpty ? firstName[0] : '';
    final last = lastName.isNotEmpty ? lastName[0] : '';
    return '$first$last'.toUpperCase();
  }
  
  User copyWith({
    int? id,
    String? username,
    String? email,
    String? firstName,
    String? lastName,
    DateTime? dateJoined,
  }) {
    return User(
      id: id ?? this.id,
      username: username ?? this.username,
      email: email ?? this.email,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      dateJoined: dateJoined ?? this.dateJoined,
    );
  }
  
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User && other.id == id;
  }
  
  @override
  int get hashCode => id.hashCode;
  
  @override
  String toString() {
    return 'User(id: $id, username: $username, email: $email)';
  }
}

class AuthResponse {
  final String access;
  final String refresh;
  final User user;
  
  const AuthResponse({
    required this.access,
    required this.refresh,
    required this.user,
  });
  
  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      access: json['access'] as String,
      refresh: json['refresh'] as String,
      user: User.fromJson(json['user'] as Map<String, dynamic>),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'access': access,
      'refresh': refresh,
      'user': user.toJson(),
    };
  }
}

class UserProfile {
  final int id;
  final User user;
  final String? phoneNumber;
  final DateTime? dateOfBirth;
  final String? profilePicture;
  final String themePreference;
  final String currency;
  final String timezone;
  final bool emailNotifications;
  final bool pushNotifications;
  final bool weeklyRecapEmail;
  final String defaultWorkspace;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  const UserProfile({
    required this.id,
    required this.user,
    this.phoneNumber,
    this.dateOfBirth,
    this.profilePicture,
    required this.themePreference,
    required this.currency,
    required this.timezone,
    required this.emailNotifications,
    required this.pushNotifications,
    required this.weeklyRecapEmail,
    required this.defaultWorkspace,
    required this.createdAt,
    required this.updatedAt,
  });
  
  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'] as int,
      user: User.fromJson(json['user'] as Map<String, dynamic>),
      phoneNumber: json['phone_number'] as String?,
      dateOfBirth: json['date_of_birth'] != null 
          ? DateTime.parse(json['date_of_birth'] as String)
          : null,
      profilePicture: json['profile_picture'] as String?,
      themePreference: json['theme_preference'] as String? ?? 'light',
      currency: json['currency'] as String? ?? 'USD',
      timezone: json['timezone'] as String? ?? 'UTC',
      emailNotifications: json['email_notifications'] as bool? ?? true,
      pushNotifications: json['push_notifications'] as bool? ?? true,
      weeklyRecapEmail: json['weekly_recap_email'] as bool? ?? true,
      defaultWorkspace: json['default_workspace'] as String? ?? 'personal',
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user': user.toJson(),
      'phone_number': phoneNumber,
      'date_of_birth': dateOfBirth?.toIso8601String(),
      'profile_picture': profilePicture,
      'theme_preference': themePreference,
      'currency': currency,
      'timezone': timezone,
      'email_notifications': emailNotifications,
      'push_notifications': pushNotifications,
      'weekly_recap_email': weeklyRecapEmail,
      'default_workspace': defaultWorkspace,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
  
  UserProfile copyWith({
    int? id,
    User? user,
    String? phoneNumber,
    DateTime? dateOfBirth,
    String? profilePicture,
    String? themePreference,
    String? currency,
    String? timezone,
    bool? emailNotifications,
    bool? pushNotifications,
    bool? weeklyRecapEmail,
    String? defaultWorkspace,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return UserProfile(
      id: id ?? this.id,
      user: user ?? this.user,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      dateOfBirth: dateOfBirth ?? this.dateOfBirth,
      profilePicture: profilePicture ?? this.profilePicture,
      themePreference: themePreference ?? this.themePreference,
      currency: currency ?? this.currency,
      timezone: timezone ?? this.timezone,
      emailNotifications: emailNotifications ?? this.emailNotifications,
      pushNotifications: pushNotifications ?? this.pushNotifications,
      weeklyRecapEmail: weeklyRecapEmail ?? this.weeklyRecapEmail,
      defaultWorkspace: defaultWorkspace ?? this.defaultWorkspace,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
