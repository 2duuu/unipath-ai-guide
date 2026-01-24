/**
 * Auto-save helper for pending quiz data after authentication
 */

import { loadPendingQuiz, clearPendingQuiz } from './pendingQuiz';
import { saveQuizAttempt } from '@/services/api';
import type { UniversityMatch, ProgramMatch } from '@/types/quiz';

export interface AutoSaveResult {
  success: boolean;
  message: string;
  error?: string;
}

/**
 * Automatically save pending quiz data after user authenticates
 * @param userId - The authenticated user's ID
 * @returns Result object with success status and message
 */
export async function autoSavePendingQuiz(userId: number): Promise<AutoSaveResult> {
  try {
    // Load pending quiz data
    const pendingData = loadPendingQuiz();
    
    if (!pendingData) {
      return {
        success: false,
        message: 'No pending quiz data found',
      };
    }

    const { quizType, answers, matches } = pendingData;

    // Extract match information
    const mainMatch = matches[0] 
      ? (quizType === 'initial' 
          ? (matches[0] as UniversityMatch).university_name 
          : (matches[0] as ProgramMatch).program_name) 
      : 'No match';
    
    const score = matches[0] 
      ? (quizType === 'initial' 
          ? (matches[0] as UniversityMatch).match_score 
          : (matches[0] as ProgramMatch).match_score) 
      : 0;
    
    const matchedList = matches.map((m: any) => m.university_name || m.program_name);

    // Save to backend
    await saveQuizAttempt({
      user_id: userId,
      quiz_type: quizType,
      num_questions: Object.keys(answers).length,
      main_match: mainMatch,
      score_percentage: score,
      matched_universities: matchedList,
      quiz_answers: answers,
    });

    // Clear pending data after successful save
    clearPendingQuiz();

    // Dispatch event to refresh quiz results in Account page
    window.dispatchEvent(new CustomEvent('quizSaved'));

    return {
      success: true,
      message: `Your ${quizType === 'initial' ? 'rapid' : 'complete'} quiz has been saved to your profile!`,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to save quiz';
    console.error('Auto-save pending quiz error:', error);
    
    // Keep the pending data in localStorage for potential retry
    return {
      success: false,
      message: 'Failed to save quiz',
      error: errorMessage,
    };
  }
}
