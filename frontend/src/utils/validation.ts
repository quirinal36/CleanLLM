/**
 * 폼 검증 유틸리티
 */

export interface ValidationResult {
  isValid: boolean;
  message?: string;
}

/**
 * 이메일 유효성 검증
 * @param email 검증할 이메일
 * @returns 검증 결과
 */
export const validateEmail = (email: string): ValidationResult => {
  if (!email.trim()) {
    return { isValid: false, message: '이메일을 입력해주세요.' };
  }

  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    return { isValid: false, message: '올바른 이메일 형식이 아닙니다.' };
  }

  return { isValid: true };
};

/**
 * 비밀번호 유효성 검증
 * - 최소 8자 이상
 * - 영문 + 숫자 조합
 * @param password 검증할 비밀번호
 * @returns 검증 결과
 */
export const validatePassword = (password: string): ValidationResult => {
  if (!password) {
    return { isValid: false, message: '비밀번호를 입력해주세요.' };
  }

  if (password.length < 8) {
    return { isValid: false, message: '비밀번호는 최소 8자 이상이어야 합니다.' };
  }

  const hasLetter = /[a-zA-Z]/.test(password);
  const hasNumber = /[0-9]/.test(password);

  if (!hasLetter || !hasNumber) {
    return { isValid: false, message: '비밀번호는 영문과 숫자를 모두 포함해야 합니다.' };
  }

  return { isValid: true };
};

/**
 * 비밀번호 확인 검증
 * @param password 원본 비밀번호
 * @param confirmPassword 확인 비밀번호
 * @returns 검증 결과
 */
export const validatePasswordConfirm = (
  password: string,
  confirmPassword: string
): ValidationResult => {
  if (!confirmPassword) {
    return { isValid: false, message: '비밀번호 확인을 입력해주세요.' };
  }

  if (password !== confirmPassword) {
    return { isValid: false, message: '비밀번호가 일치하지 않습니다.' };
  }

  return { isValid: true };
};
