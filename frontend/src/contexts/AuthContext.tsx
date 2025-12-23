/**
 * Auth Context
 * CLEAN-14: 인증 상태 Context 생성 (Frontend)
 *
 * 앱 전역에서 인증 상태를 관리하는 Context
 */

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from 'react';
import {
  User,
  AuthState,
  SignupRequest,
  LoginRequest,
  TokenResponse,
} from '../types/auth';
import { authApi, setAuthToken, AuthApiError } from '../services/authApi';
import tokenStorage from '../services/tokenStorage';

/**
 * Auth Context 값 타입
 */
interface AuthContextValue extends AuthState {
  // Actions
  signup: (data: SignupRequest) => Promise<void>;
  login: (data: LoginRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  // Utilities
  isParent: boolean;
  isChild: boolean;
}

/**
 * Auth Context 생성
 */
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

/**
 * Auth Provider Props
 */
interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Auth Provider Component
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [state, setState] = useState<AuthState>({
    isAuthenticated: false,
    isLoading: true, // 초기 로딩 상태
    user: null,
    token: null,
  });

  /**
   * 초기화: 저장된 인증 정보 복원
   */
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const authData = await tokenStorage.getAuthData();

        if (authData) {
          // 토큰 만료 확인
          const isExpired = await tokenStorage.isTokenExpired();

          if (!isExpired) {
            // 유효한 토큰이 있으면 인증 상태 복원
            setAuthToken(authData.accessToken);
            setState({
              isAuthenticated: true,
              isLoading: false,
              user: authData.user,
              token: authData.accessToken,
            });
            return;
          }
        }

        // 저장된 인증 정보가 없거나 만료됨
        await tokenStorage.clearAuthData();
        setState({
          isAuthenticated: false,
          isLoading: false,
          user: null,
          token: null,
        });
      } catch (error) {
        console.error('Auth initialization error:', error);
        setState({
          isAuthenticated: false,
          isLoading: false,
          user: null,
          token: null,
        });
      }
    };

    initializeAuth();
  }, []);

  /**
   * 인증 성공 처리
   */
  const handleAuthSuccess = useCallback(async (response: TokenResponse) => {
    try {
      // 토큰 및 사용자 정보 저장
      await tokenStorage.saveAuthData(
        response.access_token,
        response.expires_in,
        response.user
      );

      // API 클라이언트에 토큰 설정
      setAuthToken(response.access_token);

      // 상태 업데이트
      setState({
        isAuthenticated: true,
        isLoading: false,
        user: response.user,
        token: response.access_token,
      });
    } catch (error) {
      console.error('Failed to handle auth success:', error);
      throw error;
    }
  }, []);

  /**
   * 회원가입
   */
  const signup = useCallback(
    async (data: SignupRequest) => {
      setState((prev) => ({ ...prev, isLoading: true }));

      try {
        const response = await authApi.signup(data);
        await handleAuthSuccess(response);
      } catch (error) {
        setState((prev) => ({ ...prev, isLoading: false }));
        throw error;
      }
    },
    [handleAuthSuccess]
  );

  /**
   * 로그인
   */
  const login = useCallback(
    async (data: LoginRequest) => {
      setState((prev) => ({ ...prev, isLoading: true }));

      try {
        const response = await authApi.login(data);
        await handleAuthSuccess(response);
      } catch (error) {
        setState((prev) => ({ ...prev, isLoading: false }));
        throw error;
      }
    },
    [handleAuthSuccess]
  );

  /**
   * 로그아웃
   */
  const logout = useCallback(async () => {
    try {
      // 저장된 인증 데이터 삭제
      await tokenStorage.clearAuthData();

      // API 클라이언트에서 토큰 제거
      setAuthToken(null);

      // 상태 초기화
      setState({
        isAuthenticated: false,
        isLoading: false,
        user: null,
        token: null,
      });
    } catch (error) {
      console.error('Logout error:', error);
      // 에러가 발생해도 로그아웃 상태로 전환
      setState({
        isAuthenticated: false,
        isLoading: false,
        user: null,
        token: null,
      });
    }
  }, []);

  /**
   * 사용자 정보 새로고침
   */
  const refreshUser = useCallback(async () => {
    if (!state.token) {
      return;
    }

    try {
      const user = await authApi.getMe();

      // 저장소 및 상태 업데이트
      await tokenStorage.saveUser(user);
      setState((prev) => ({
        ...prev,
        user,
      }));
    } catch (error) {
      console.error('Failed to refresh user:', error);

      // 인증 에러 (401)인 경우 로그아웃
      if (error instanceof AuthApiError && error.statusCode === 401) {
        await logout();
      }

      throw error;
    }
  }, [state.token, logout]);

  /**
   * Derived state
   */
  const isParent = state.user?.role === 'parent';
  const isChild = state.user?.role === 'child';

  /**
   * Context value
   */
  const contextValue: AuthContextValue = {
    ...state,
    signup,
    login,
    logout,
    refreshUser,
    isParent,
    isChild,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}

/**
 * useAuth Hook
 * Auth Context를 사용하는 커스텀 훅
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}

/**
 * withAuth HOC
 * 인증이 필요한 컴포넌트를 위한 HOC
 */
export function withAuth<P extends object>(
  WrappedComponent: React.ComponentType<P>
): React.FC<P> {
  return function WithAuthComponent(props: P) {
    const { isAuthenticated, isLoading } = useAuth();

    if (isLoading) {
      // 로딩 중일 때는 null 반환 (또는 로딩 컴포넌트)
      return null;
    }

    if (!isAuthenticated) {
      // 인증되지 않은 경우 null 반환 (또는 리다이렉트)
      return null;
    }

    return <WrappedComponent {...props} />;
  };
}

export default AuthContext;
