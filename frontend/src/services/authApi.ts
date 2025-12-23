/**
 * Auth API Service
 * CLEAN-13: Auth API Service 구현 (Frontend)
 *
 * Backend Auth API와 통신하는 서비스 레이어
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  SignupRequest,
  LoginRequest,
  LinkChildRequest,
  TokenResponse,
  ParentChildLinkResponse,
  ChildListResponse,
  SuccessResponse,
  User,
  ApiError,
} from '../types/auth';

// API Base URL (환경 변수에서 가져오거나 기본값 사용)
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

/**
 * API 에러 클래스
 */
export class AuthApiError extends Error {
  public statusCode: number;
  public errorCode?: string;

  constructor(message: string, statusCode: number, errorCode?: string) {
    super(message);
    this.name = 'AuthApiError';
    this.statusCode = statusCode;
    this.errorCode = errorCode;
  }
}

/**
 * Axios 인스턴스 생성
 */
const createApiClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: `${API_BASE_URL}${API_VERSION}`,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // 응답 인터셉터: 에러 처리
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError<ApiError>) => {
      if (error.response) {
        const { status, data } = error.response;
        const message = data?.detail || '요청 처리 중 오류가 발생했습니다.';
        const errorCode = data?.error_code;
        throw new AuthApiError(message, status, errorCode);
      } else if (error.request) {
        throw new AuthApiError('서버에 연결할 수 없습니다. 네트워크를 확인해주세요.', 0);
      } else {
        throw new AuthApiError(error.message || '알 수 없는 오류가 발생했습니다.', 0);
      }
    }
  );

  return client;
};

// API 클라이언트 인스턴스
let apiClient = createApiClient();

/**
 * 인증 토큰 설정
 * @param token JWT 액세스 토큰
 */
export const setAuthToken = (token: string | null): void => {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common['Authorization'];
  }
};

/**
 * API 클라이언트 재설정 (테스트 등에서 사용)
 */
export const resetApiClient = (): void => {
  apiClient = createApiClient();
};

/**
 * Auth API 서비스
 */
export const authApi = {
  /**
   * 회원가입
   * @param data 회원가입 정보 (email, password, role)
   * @returns 토큰 및 사용자 정보
   */
  signup: async (data: SignupRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/signup', data);
    return response.data;
  },

  /**
   * 로그인
   * @param data 로그인 정보 (email, password)
   * @returns 토큰 및 사용자 정보
   */
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/login', data);
    return response.data;
  },

  /**
   * 현재 사용자 정보 조회
   * @returns 사용자 정보
   */
  getMe: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  /**
   * 자녀 계정 연동 (부모 전용)
   * @param data 연동할 자녀 ID
   * @returns 연동 정보
   */
  linkChild: async (data: LinkChildRequest): Promise<ParentChildLinkResponse> => {
    const response = await apiClient.post<ParentChildLinkResponse>(
      '/auth/link-child',
      data
    );
    return response.data;
  },

  /**
   * 연동된 자녀 목록 조회 (부모 전용)
   * @returns 자녀 목록
   */
  getChildren: async (): Promise<ChildListResponse> => {
    const response = await apiClient.get<ChildListResponse>('/auth/children');
    return response.data;
  },

  /**
   * 자녀 연동 해제 (부모 전용)
   * @param childId 연동 해제할 자녀 ID
   * @returns 성공 메시지
   */
  unlinkChild: async (childId: number): Promise<SuccessResponse> => {
    const response = await apiClient.delete<SuccessResponse>(
      `/auth/link-child/${childId}`
    );
    return response.data;
  },

  /**
   * 인증 서비스 상태 확인
   * @returns 서비스 상태
   */
  healthCheck: async (): Promise<{ status: string; service: string }> => {
    const response = await apiClient.get<{ status: string; service: string }>(
      '/auth/health'
    );
    return response.data;
  },
};

export default authApi;
