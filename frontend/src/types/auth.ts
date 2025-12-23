/**
 * Auth 관련 타입 정의
 */

// User role type
export type UserRole = 'parent' | 'child';

// Form data types
export interface SignupFormData {
  email: string;
  password: string;
  confirmPassword: string;
  role: UserRole;
}

export interface LoginFormData {
  email: string;
  password: string;
}

// API request types
export interface SignupRequest {
  email: string;
  password: string;
  role: UserRole;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LinkChildRequest {
  child_id: number;
}

// User types
export interface User {
  id: number;
  email: string;
  role: UserRole;
  created_at: string;
  updated_at: string;
}

// API response types
export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface ParentChildLinkResponse {
  id: number;
  parent_id: number;
  child_id: number;
  linked_at: string;
}

export interface ChildListResponse {
  children: User[];
  total: number;
  max_allowed: number;
}

export interface SuccessResponse {
  message: string;
  data?: Record<string, unknown>;
}

// Error types
export interface ApiError {
  detail: string;
  error_code?: string;
}

export interface ValidationError {
  field: string;
  message: string;
}

// Auth state types (for context)
export interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
  token: string | null;
}
