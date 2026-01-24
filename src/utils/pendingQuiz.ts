/**
 * Utility functions for managing pending quiz saves in localStorage
 * Used when non-authenticated users try to save quiz results
 */

import type { Match } from '@/types/quiz';

const PENDING_QUIZ_KEY = 'pendingQuizSave';
const EXPIRATION_TIME = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

export interface PendingQuizData {
  quizType: 'initial' | 'extended';
  answers: Record<string, any>;
  matches: Match[];
  profileId: number | null;
  timestamp: number;
}

/**
 * Save quiz data to localStorage for later retrieval after login
 */
export function savePendingQuiz(data: Omit<PendingQuizData, 'timestamp'>): void {
  try {
    const pendingData: PendingQuizData = {
      ...data,
      timestamp: Date.now(),
    };
    localStorage.setItem(PENDING_QUIZ_KEY, JSON.stringify(pendingData));
  } catch (error) {
    console.error('Failed to save pending quiz:', error);
  }
}

/**
 * Retrieve pending quiz data from localStorage
 * Returns null if no data exists or if data has expired
 */
export function loadPendingQuiz(): PendingQuizData | null {
  try {
    const saved = localStorage.getItem(PENDING_QUIZ_KEY);
    if (!saved) return null;

    const data: PendingQuizData = JSON.parse(saved);
    
    // Check if data has expired (older than 24 hours)
    const isExpired = Date.now() - data.timestamp > EXPIRATION_TIME;
    if (isExpired) {
      clearPendingQuiz();
      return null;
    }

    return data;
  } catch (error) {
    console.error('Failed to load pending quiz:', error);
    clearPendingQuiz(); // Clear corrupted data
    return null;
  }
}

/**
 * Clear pending quiz data from localStorage
 */
export function clearPendingQuiz(): void {
  try {
    localStorage.removeItem(PENDING_QUIZ_KEY);
  } catch (error) {
    console.error('Failed to clear pending quiz:', error);
  }
}

/**
 * Check if there's a pending quiz save in localStorage
 */
export function hasPendingQuiz(): boolean {
  return loadPendingQuiz() !== null;
}
