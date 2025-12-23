/**
 * Token Storage Service
 * CLEAN-14: 토큰 저장 및 관리 로직 구현 (Frontend)
 *
 * AsyncStorage를 사용한 JWT 토큰 저장 및 관리
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import { User } from '../types/auth';

// Storage keys
const STORAGE_KEYS = {
  ACCESS_TOKEN: '@eduguard_access_token',
  USER_DATA: '@eduguard_user_data',
  TOKEN_EXPIRY: '@eduguard_token_expiry',
} as const;

/**
 * Token storage interface
 */
export interface StoredAuthData {
  accessToken: string;
  user: User;
  expiresAt: number; // Unix timestamp
}

/**
 * 토큰 저장
 * @param accessToken JWT 액세스 토큰
 * @param expiresIn 만료 시간 (초)
 */
export const saveToken = async (
  accessToken: string,
  expiresIn: number
): Promise<void> => {
  try {
    const expiresAt = Date.now() + expiresIn * 1000;
    await AsyncStorage.multiSet([
      [STORAGE_KEYS.ACCESS_TOKEN, accessToken],
      [STORAGE_KEYS.TOKEN_EXPIRY, expiresAt.toString()],
    ]);
  } catch (error) {
    console.error('Failed to save token:', error);
    throw new Error('토큰 저장에 실패했습니다.');
  }
};

/**
 * 토큰 조회
 * @returns 저장된 토큰 또는 null
 */
export const getToken = async (): Promise<string | null> => {
  try {
    const token = await AsyncStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    return token;
  } catch (error) {
    console.error('Failed to get token:', error);
    return null;
  }
};

/**
 * 토큰 만료 여부 확인
 * @returns 토큰이 만료되었으면 true
 */
export const isTokenExpired = async (): Promise<boolean> => {
  try {
    const expiryString = await AsyncStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRY);
    if (!expiryString) {
      return true;
    }

    const expiresAt = parseInt(expiryString, 10);
    // 만료 5분 전부터 만료된 것으로 처리 (버퍼)
    const bufferMs = 5 * 60 * 1000;
    return Date.now() > expiresAt - bufferMs;
  } catch (error) {
    console.error('Failed to check token expiry:', error);
    return true;
  }
};

/**
 * 유효한 토큰 조회 (만료되지 않은 경우에만 반환)
 * @returns 유효한 토큰 또는 null
 */
export const getValidToken = async (): Promise<string | null> => {
  try {
    const isExpired = await isTokenExpired();
    if (isExpired) {
      // 만료된 토큰은 삭제
      await removeToken();
      return null;
    }
    return await getToken();
  } catch (error) {
    console.error('Failed to get valid token:', error);
    return null;
  }
};

/**
 * 토큰 삭제 (로그아웃)
 */
export const removeToken = async (): Promise<void> => {
  try {
    await AsyncStorage.multiRemove([
      STORAGE_KEYS.ACCESS_TOKEN,
      STORAGE_KEYS.TOKEN_EXPIRY,
    ]);
  } catch (error) {
    console.error('Failed to remove token:', error);
    throw new Error('토큰 삭제에 실패했습니다.');
  }
};

/**
 * 사용자 정보 저장
 * @param user 사용자 정보
 */
export const saveUser = async (user: User): Promise<void> => {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
  } catch (error) {
    console.error('Failed to save user:', error);
    throw new Error('사용자 정보 저장에 실패했습니다.');
  }
};

/**
 * 사용자 정보 조회
 * @returns 저장된 사용자 정보 또는 null
 */
export const getUser = async (): Promise<User | null> => {
  try {
    const userJson = await AsyncStorage.getItem(STORAGE_KEYS.USER_DATA);
    if (!userJson) {
      return null;
    }
    return JSON.parse(userJson) as User;
  } catch (error) {
    console.error('Failed to get user:', error);
    return null;
  }
};

/**
 * 사용자 정보 삭제
 */
export const removeUser = async (): Promise<void> => {
  try {
    await AsyncStorage.removeItem(STORAGE_KEYS.USER_DATA);
  } catch (error) {
    console.error('Failed to remove user:', error);
    throw new Error('사용자 정보 삭제에 실패했습니다.');
  }
};

/**
 * 인증 데이터 저장 (토큰 + 사용자 정보)
 * @param accessToken JWT 액세스 토큰
 * @param expiresIn 만료 시간 (초)
 * @param user 사용자 정보
 */
export const saveAuthData = async (
  accessToken: string,
  expiresIn: number,
  user: User
): Promise<void> => {
  try {
    const expiresAt = Date.now() + expiresIn * 1000;
    await AsyncStorage.multiSet([
      [STORAGE_KEYS.ACCESS_TOKEN, accessToken],
      [STORAGE_KEYS.TOKEN_EXPIRY, expiresAt.toString()],
      [STORAGE_KEYS.USER_DATA, JSON.stringify(user)],
    ]);
  } catch (error) {
    console.error('Failed to save auth data:', error);
    throw new Error('인증 데이터 저장에 실패했습니다.');
  }
};

/**
 * 인증 데이터 조회
 * @returns 저장된 인증 데이터 또는 null
 */
export const getAuthData = async (): Promise<StoredAuthData | null> => {
  try {
    const [[, accessToken], [, expiryString], [, userJson]] =
      await AsyncStorage.multiGet([
        STORAGE_KEYS.ACCESS_TOKEN,
        STORAGE_KEYS.TOKEN_EXPIRY,
        STORAGE_KEYS.USER_DATA,
      ]);

    if (!accessToken || !expiryString || !userJson) {
      return null;
    }

    const expiresAt = parseInt(expiryString, 10);
    const user = JSON.parse(userJson) as User;

    return {
      accessToken,
      user,
      expiresAt,
    };
  } catch (error) {
    console.error('Failed to get auth data:', error);
    return null;
  }
};

/**
 * 모든 인증 데이터 삭제 (로그아웃)
 */
export const clearAuthData = async (): Promise<void> => {
  try {
    await AsyncStorage.multiRemove([
      STORAGE_KEYS.ACCESS_TOKEN,
      STORAGE_KEYS.TOKEN_EXPIRY,
      STORAGE_KEYS.USER_DATA,
    ]);
  } catch (error) {
    console.error('Failed to clear auth data:', error);
    throw new Error('인증 데이터 삭제에 실패했습니다.');
  }
};

/**
 * 토큰 만료까지 남은 시간 (밀리초)
 * @returns 남은 시간 또는 0 (이미 만료된 경우)
 */
export const getTokenRemainingTime = async (): Promise<number> => {
  try {
    const expiryString = await AsyncStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRY);
    if (!expiryString) {
      return 0;
    }

    const expiresAt = parseInt(expiryString, 10);
    const remaining = expiresAt - Date.now();
    return remaining > 0 ? remaining : 0;
  } catch (error) {
    console.error('Failed to get token remaining time:', error);
    return 0;
  }
};

// Default export for convenience
const tokenStorage = {
  saveToken,
  getToken,
  isTokenExpired,
  getValidToken,
  removeToken,
  saveUser,
  getUser,
  removeUser,
  saveAuthData,
  getAuthData,
  clearAuthData,
  getTokenRemainingTime,
};

export default tokenStorage;
