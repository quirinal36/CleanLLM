/**
 * Auth 관련 타입 정의
 */

export interface SignupFormData {
  email: string;
  password: string;
  confirmPassword: string;
  role: 'parent' | 'child';
}

export interface LoginFormData {
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: {
    id: number;
    email: string;
    role: 'parent' | 'child';
  };
}

export interface ValidationError {
  field: string;
  message: string;
}
