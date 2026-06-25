export interface User {
  id: number;

  username: string;

  email: string;

  created_at: string;
}

export interface LoginRequest {
  username: string;

  password: string;
}

export interface RegisterRequest {
  username: string;

  email: string;

  password: string;

  confirmPassword: string;
}

export interface AuthResponse {
  access: string;

  refresh: string;

  user: User;
}
