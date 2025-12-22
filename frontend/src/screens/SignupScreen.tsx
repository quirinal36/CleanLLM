/**
 * 회원가입 화면
 * CLEAN-11: 회원가입 화면 UI 구현 (Frontend)
 */

import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  ScrollView,
  Platform,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { colors, spacing, borderRadius, fontSize } from '../styles/colors';
import {
  validateEmail,
  validatePassword,
  validatePasswordConfirm,
} from '../utils/validation';

interface FormErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
}

export default function SignupScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState<'parent' | 'child'>('child');
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  /**
   * 폼 검증
   */
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // 이메일 검증
    const emailValidation = validateEmail(email);
    if (!emailValidation.isValid) {
      newErrors.email = emailValidation.message;
    }

    // 비밀번호 검증
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.isValid) {
      newErrors.password = passwordValidation.message;
    }

    // 비밀번호 확인 검증
    const confirmPasswordValidation = validatePasswordConfirm(password, confirmPassword);
    if (!confirmPasswordValidation.isValid) {
      newErrors.confirmPassword = confirmPasswordValidation.message;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * 회원가입 처리
   */
  const handleSignup = async () => {
    // 폼 검증
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // TODO: API 연동 (CLEAN-13에서 구현 예정)
      // await authApi.signup({ email, password, role });

      // 임시: 성공 메시지
      Alert.alert(
        '회원가입 성공',
        '환영합니다! 로그인 화면으로 이동합니다.',
        [{ text: '확인' }]
      );
    } catch (error) {
      Alert.alert(
        '회원가입 실패',
        error instanceof Error ? error.message : '회원가입 중 오류가 발생했습니다.',
        [{ text: '확인' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * 입력 필드 변경 시 해당 에러 초기화
   */
  const handleEmailChange = (text: string) => {
    setEmail(text);
    if (errors.email) {
      setErrors({ ...errors, email: undefined });
    }
  };

  const handlePasswordChange = (text: string) => {
    setPassword(text);
    if (errors.password) {
      setErrors({ ...errors, password: undefined });
    }
  };

  const handleConfirmPasswordChange = (text: string) => {
    setConfirmPassword(text);
    if (errors.confirmPassword) {
      setErrors({ ...errors, confirmPassword: undefined });
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <StatusBar style="dark" />
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.content}>
          {/* 헤더 */}
          <View style={styles.header}>
            <Text style={styles.title}>회원가입</Text>
            <Text style={styles.subtitle}>EduGuard AI와 함께 안전하게 학습하세요</Text>
          </View>

          {/* 역할 선택 */}
          <View style={styles.roleContainer}>
            <Text style={styles.label}>가입 유형</Text>
            <View style={styles.roleButtons}>
              <TouchableOpacity
                style={[
                  styles.roleButton,
                  role === 'child' && styles.roleButtonActive,
                ]}
                onPress={() => setRole('child')}
                activeOpacity={0.7}
              >
                <Text
                  style={[
                    styles.roleButtonText,
                    role === 'child' && styles.roleButtonTextActive,
                  ]}
                >
                  학생 👦
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[
                  styles.roleButton,
                  role === 'parent' && styles.roleButtonActive,
                ]}
                onPress={() => setRole('parent')}
                activeOpacity={0.7}
              >
                <Text
                  style={[
                    styles.roleButtonText,
                    role === 'parent' && styles.roleButtonTextActive,
                  ]}
                >
                  부모 👨‍👩‍👧
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* 이메일 입력 */}
          <View style={styles.inputContainer}>
            <Text style={styles.label}>이메일</Text>
            <TextInput
              style={[styles.input, errors.email && styles.inputError]}
              placeholder="example@email.com"
              placeholderTextColor={colors.textLight}
              value={email}
              onChangeText={handleEmailChange}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />
            {errors.email && <Text style={styles.errorText}>{errors.email}</Text>}
          </View>

          {/* 비밀번호 입력 */}
          <View style={styles.inputContainer}>
            <Text style={styles.label}>비밀번호</Text>
            <TextInput
              style={[styles.input, errors.password && styles.inputError]}
              placeholder="최소 8자, 영문+숫자 조합"
              placeholderTextColor={colors.textLight}
              value={password}
              onChangeText={handlePasswordChange}
              secureTextEntry
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />
            {errors.password && <Text style={styles.errorText}>{errors.password}</Text>}
          </View>

          {/* 비밀번호 확인 입력 */}
          <View style={styles.inputContainer}>
            <Text style={styles.label}>비밀번호 확인</Text>
            <TextInput
              style={[styles.input, errors.confirmPassword && styles.inputError]}
              placeholder="비밀번호를 다시 입력하세요"
              placeholderTextColor={colors.textLight}
              value={confirmPassword}
              onChangeText={handleConfirmPasswordChange}
              secureTextEntry
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />
            {errors.confirmPassword && (
              <Text style={styles.errorText}>{errors.confirmPassword}</Text>
            )}
          </View>

          {/* 회원가입 버튼 */}
          <TouchableOpacity
            style={[styles.signupButton, isLoading && styles.signupButtonDisabled]}
            onPress={handleSignup}
            disabled={isLoading}
            activeOpacity={0.8}
          >
            {isLoading ? (
              <ActivityIndicator color={colors.textWhite} />
            ) : (
              <Text style={styles.signupButtonText}>회원가입</Text>
            )}
          </TouchableOpacity>

          {/* 로그인 링크 */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>이미 계정이 있으신가요?</Text>
            <TouchableOpacity
              onPress={() => {
                // TODO: 로그인 화면으로 이동 (Navigation 설정 후)
                Alert.alert('안내', '로그인 화면으로 이동합니다.');
              }}
              disabled={isLoading}
            >
              <Text style={styles.footerLink}>로그인</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    flexGrow: 1,
  },
  content: {
    flex: 1,
    padding: spacing.lg,
    justifyContent: 'center',
  },
  header: {
    marginBottom: spacing.xl,
    alignItems: 'center',
  },
  title: {
    fontSize: fontSize.xxl,
    fontWeight: 'bold',
    color: colors.textPrimary,
    marginBottom: spacing.sm,
  },
  subtitle: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  roleContainer: {
    marginBottom: spacing.lg,
  },
  label: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: spacing.sm,
  },
  roleButtons: {
    flexDirection: 'row',
    gap: spacing.md,
  },
  roleButton: {
    flex: 1,
    height: 50,
    backgroundColor: colors.surface,
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: borderRadius.lg,
    justifyContent: 'center',
    alignItems: 'center',
  },
  roleButtonActive: {
    backgroundColor: colors.primaryLight,
    borderColor: colors.primary,
  },
  roleButtonText: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    fontWeight: '600',
  },
  roleButtonTextActive: {
    color: colors.primary,
  },
  inputContainer: {
    marginBottom: spacing.lg,
  },
  input: {
    height: 50,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    fontSize: fontSize.md,
    color: colors.textPrimary,
  },
  inputError: {
    borderColor: colors.error,
  },
  errorText: {
    fontSize: fontSize.sm,
    color: colors.error,
    marginTop: spacing.xs,
    marginLeft: spacing.xs,
  },
  signupButton: {
    height: 50,
    backgroundColor: colors.primary,
    borderRadius: borderRadius.lg,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: spacing.md,
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  signupButtonDisabled: {
    backgroundColor: colors.textLight,
  },
  signupButtonText: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.textWhite,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: spacing.xl,
    gap: spacing.xs,
  },
  footerText: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
  },
  footerLink: {
    fontSize: fontSize.md,
    color: colors.primary,
    fontWeight: '600',
  },
});
