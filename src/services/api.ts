/**
 * API service for UniHub backend integration
 */
import axios, { AxiosError } from 'axios';
import type {
  InitialQuizResponse,
  InitialSubmitRequest,
  InitialSubmitResponse,
  ExtendedQuizResponse,
  ExtendedSubmitRequest,
  ExtendedSubmitResponse,
  FeedbackRequest,
  FeedbackResponse,
  StatsResponse,
} from '@/types/quiz';

// Get API base URL from environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8084';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handling helper
const handleApiError = (error: unknown): never => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail: string }>;
    const message = axiosError.response?.data?.detail || axiosError.message || 'An error occurred';
    throw new Error(message);
  }
  throw new Error('An unexpected error occurred');
};

/**
 * Health check endpoint
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get initial quiz questions (13 questions)
 */
export const getInitialQuestions = async (): Promise<InitialQuizResponse> => {
  try {
    const response = await api.get<InitialQuizResponse>('/api/questions/initial');
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Submit initial quiz answers and get university matches
 */
export const submitInitialQuiz = async (
  data: InitialSubmitRequest & { user_id?: number }
): Promise<InitialSubmitResponse> => {
  try {
    const response = await api.post<InitialSubmitResponse>('/api/submit/initial', data);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get extended quiz questions (12-13 questions)
 */
export const getExtendedQuestions = async (profileId: number): Promise<ExtendedQuizResponse> => {
  try {
    const response = await api.get<ExtendedQuizResponse>('/api/questions/extended', {
      params: { profile_id: profileId },
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Submit extended quiz answers and get program matches
 */
export const submitExtendedQuiz = async (
  data: ExtendedSubmitRequest
): Promise<ExtendedSubmitResponse> => {
  try {
    const response = await api.post<ExtendedSubmitResponse>('/api/submit/extended', data);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Submit user feedback
 */
export const submitFeedback = async (
  feedback: FeedbackRequest
): Promise<FeedbackResponse> => {
  try {
    const response = await api.post<FeedbackResponse>('/api/feedback', feedback);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get current user's quiz results
 */
export const getUserQuizResults = async (): Promise<any> => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await api.get('/api/quiz/results', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get user's saved quiz attempts
 */
export const getUserQuizAttempts = async (): Promise<any> => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await api.get('/api/quiz/attempts', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Save a quiz attempt to user profile
 */
export const saveQuizAttempt = async (data: any): Promise<any> => {
  try {
    const response = await api.post('/api/quiz/save-attempt', data);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get database statistics
 */
export const getStats = async (): Promise<StatsResponse> => {
  try {
    const response = await api.get<StatsResponse>('/api/stats');
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export default api;
