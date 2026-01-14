// Advanced Usage Examples for UniHub Frontend

import { useState, useEffect } from 'react';
import { UniHubAPI, Question, Match, isProgramMatch } from './types';

// ==================================================
// Example 1: Custom Hook for Quiz Management
// ==================================================

export function useQuiz() {
  const [api] = useState(() => new UniHubAPI());
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadInitialQuestions = async () => {
    setLoading(true);
    try {
      const data = await api.getInitialQuestions();
      setQuestions(data.questions);
      setError(null);
    } catch (err) {
      setError('Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = (questionId: string, answer: any) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const nextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const previousQuestion = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  };

  const submitQuiz = async () => {
    setLoading(true);
    try {
      const answerArray = Object.entries(answers).map(([question_id, answer]) => ({
        question_id,
        answer
      }));
      const result = await api.submitInitialQuiz(answerArray);
      setError(null);
      return result;
    } catch (err) {
      setError('Failed to submit quiz');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    questions,
    currentQuestion: questions[currentIndex],
    currentIndex,
    answers,
    loading,
    error,
    loadInitialQuestions,
    submitAnswer,
    nextQuestion,
    previousQuestion,
    submitQuiz,
    progress: questions.length ? ((currentIndex + 1) / questions.length) * 100 : 0
  };
}

// Usage:
// const quiz = useQuiz();
// useEffect(() => { quiz.loadInitialQuestions(); }, []);

// ==================================================
// Example 2: Match Filtering and Sorting
// ==================================================

export function useMatches(initialMatches: Match[]) {
  const [matches, setMatches] = useState(initialMatches);
  const [sortBy, setSortBy] = useState<'score' | 'name' | 'type'>('score');
  const [filterType, setFilterType] = useState<'all' | 'safety' | 'target' | 'reach'>('all');

  const sortedAndFiltered = matches
    .filter(m => filterType === 'all' || m.match_type === filterType)
    .sort((a, b) => {
      switch (sortBy) {
        case 'score':
          return b.match_score - a.match_score;
        case 'name':
          const nameA = isProgramMatch(a) ? a.program_name : a.university_name;
          const nameB = isProgramMatch(b) ? b.program_name : b.university_name;
          return nameA.localeCompare(nameB);
        case 'type':
          const order = { safety: 0, target: 1, reach: 2 };
          return order[a.match_type] - order[b.match_type];
        default:
          return 0;
      }
    });

  return {
    matches: sortedAndFiltered,
    setMatches,
    sortBy,
    setSortBy,
    filterType,
    setFilterType,
    safetyCount: matches.filter(m => m.match_type === 'safety').length,
    targetCount: matches.filter(m => m.match_type === 'target').length,
    reachCount: matches.filter(m => m.match_type === 'reach').length
  };
}

// ==================================================
// Example 3: Save/Load Progress (LocalStorage)
// ==================================================

export function useSaveProgress() {
  const saveProgress = (profileId: number, answers: Record<string, any>, step: string) => {
    const data = { profileId, answers, step, timestamp: Date.now() };
    localStorage.setItem('unihub_progress', JSON.stringify(data));
  };

  const loadProgress = () => {
    const saved = localStorage.getItem('unihub_progress');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return null;
      }
    }
    return null;
  };

  const clearProgress = () => {
    localStorage.removeItem('unihub_progress');
  };

  return { saveProgress, loadProgress, clearProgress };
}

// ==================================================
// Example 4: Multi-Step Form with Context
// ==================================================

import { createContext, useContext, ReactNode } from 'react';

interface QuizContextType {
  profileId: number | null;
  setProfileId: (id: number) => void;
  matches: Match[];
  setMatches: (matches: Match[]) => void;
  api: UniHubAPI;
}

const QuizContext = createContext<QuizContextType | null>(null);

export function QuizProvider({ children }: { children: ReactNode }) {
  const [profileId, setProfileId] = useState<number | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);
  const [api] = useState(() => new UniHubAPI());

  return (
    <QuizContext.Provider value={{ profileId, setProfileId, matches, setMatches, api }}>
      {children}
    </QuizContext.Provider>
  );
}

export function useQuizContext() {
  const context = useContext(QuizContext);
  if (!context) {
    throw new Error('useQuizContext must be used within QuizProvider');
  }
  return context;
}

// Usage:
// <QuizProvider>
//   <Quiz />
// </QuizProvider>

// ==================================================
// Example 5: Shareable Results
// ==================================================

export function useShareResults() {
  const shareResults = (matches: Match[], profileId: number) => {
    const summary = matches
      .slice(0, 3)
      .map((m, i) => `${i + 1}. ${isProgramMatch(m) ? m.program_name : m.university_name} (${m.match_score.toFixed(0)}%)`)
      .join('\n');

    const text = `My UniHub matches:\n\n${summary}\n\nFind yours at: https://unihub.com/quiz`;

    if (navigator.share) {
      navigator.share({
        title: 'My University Matches',
        text: text
      });
    } else {
      navigator.clipboard.writeText(text);
      alert('Results copied to clipboard!');
    }
  };

  const generateResultsURL = (profileId: number) => {
    return `https://unihub.com/results/${profileId}`;
  };

  return { shareResults, generateResultsURL };
}

// ==================================================
// Example 6: Match Comparison Component
// ==================================================

interface ComparisonProps {
  matches: Match[];
}

export function MatchComparison({ matches }: ComparisonProps) {
  const [selected, setSelected] = useState<Match[]>([]);

  const toggleSelection = (match: Match) => {
    const id = isProgramMatch(match) ? match.program_id : match.university_name;
    const isSelected = selected.some(m => 
      isProgramMatch(m) ? m.program_id === id : m.university_name === id
    );

    if (isSelected) {
      setSelected(selected.filter(m => 
        isProgramMatch(m) ? m.program_id !== id : m.university_name !== id
      ));
    } else if (selected.length < 3) {
      setSelected([...selected, match]);
    }
  };

  return (
    <div className="comparison-container">
      <h2>Compare Matches (Select up to 3)</h2>
      <div className="comparison-grid">
        {selected.map((match, i) => (
          <div key={i} className="comparison-card">
            <h3>{isProgramMatch(match) ? match.program_name : match.university_name}</h3>
            <div>Score: {match.match_score.toFixed(0)}</div>
            <div>Type: {match.match_type}</div>
            {isProgramMatch(match) && (
              <>
                <div>Duration: {match.duration_years} years</div>
                <div>Language: {match.language}</div>
              </>
            )}
            <button onClick={() => toggleSelection(match)}>Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
}

// ==================================================
// Example 7: Analytics Tracking
// ==================================================

export function useAnalytics() {
  const trackQuizStart = () => {
    // Google Analytics, Mixpanel, etc.
    console.log('Quiz started');
  };

  const trackQuizComplete = (profileId: number, matchCount: number) => {
    console.log(`Quiz completed: Profile ${profileId}, ${matchCount} matches`);
  };

  const trackFeedback = (rating: number, helpful: boolean) => {
    console.log(`Feedback: Rating ${rating}, Helpful: ${helpful}`);
  };

  return { trackQuizStart, trackQuizComplete, trackFeedback };
}

// ==================================================
// Example 8: Error Boundary
// ==================================================

import { Component, ErrorInfo } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class QuizErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Quiz error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>Reload</button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage:
// <QuizErrorBoundary>
//   <Quiz />
// </QuizErrorBoundary>

// ==================================================
// Example 9: Responsive Match Cards
// ==================================================

interface MatchCardProps {
  match: Match;
  onSelect?: () => void;
  selected?: boolean;
}

export function MatchCard({ match, onSelect, selected }: MatchCardProps) {
  const isProgram = isProgramMatch(match);
  const name = isProgram ? match.program_name : match.university_name;
  const location = isProgram ? match.university_location : match.location;

  return (
    <div className={`match-card ${selected ? 'selected' : ''}`} onClick={onSelect}>
      <div className="match-card-header">
        <h3>{name}</h3>
        <span className={`badge ${match.match_type}`}>
          {match.match_type.toUpperCase()}
        </span>
      </div>
      
      <div className="match-score">{match.match_score.toFixed(0)}</div>
      
      <div className="match-details">
        <p>📍 {location}</p>
        {isProgram && (
          <>
            <p>🎓 {match.degree_level} ({match.duration_years}y)</p>
            <p>🗣️ {match.language}</p>
            <p>💰 €{match.tuition_annual.toLocaleString()}/year</p>
          </>
        )}
      </div>
      
      <p className="match-reasoning">{match.reasoning}</p>
    </div>
  );
}

// ==================================================
// Example 10: Keyboard Navigation
// ==================================================

export function useKeyboardNavigation(
  onNext: () => void,
  onPrevious: () => void,
  canGoNext: boolean,
  canGoPrevious: boolean
) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' && canGoNext) {
        onNext();
      } else if (e.key === 'ArrowLeft' && canGoPrevious) {
        onPrevious();
      } else if (e.key === 'Enter' && canGoNext) {
        onNext();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onNext, onPrevious, canGoNext, canGoPrevious]);
}

// Usage in Quiz component:
// useKeyboardNavigation(handleNext, handlePrevious, !!currentAnswer, currentIndex > 0);
