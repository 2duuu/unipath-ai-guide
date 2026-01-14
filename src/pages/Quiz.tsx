import { useState, useEffect } from 'react';
import {
  getInitialQuestions,
  submitInitialQuiz,
  getExtendedQuestions,
  submitExtendedQuiz,
  submitFeedback,
} from '@/services/api';
import type {
  Question,
  Answer,
  Match,
  UniversityMatch,
  ProgramMatch,
} from '@/types/quiz';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import './Quiz.css';

export default function Quiz() {
  // State management
  const [step, setStep] = useState<'initial' | 'results' | 'extended' | 'program-results' | 'feedback'>('initial');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [profileId, setProfileId] = useState<number | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);
  const [matchType, setMatchType] = useState<'university' | 'program'>('university');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Feedback state
  const [rating, setRating] = useState(0);
  const [helpful, setHelpful] = useState<boolean | null>(null);
  const [comments, setComments] = useState('');

  // Fetch initial questions on mount
  useEffect(() => {
    fetchInitialQuestions();
  }, []);

  const fetchInitialQuestions = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getInitialQuestions();
      setQuestions(data.questions);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const fetchExtendedQuestions = async (profileId: number) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getExtendedQuestions(profileId);
      setQuestions(data.questions);
      setCurrentQuestionIndex(0);
      setAnswers({});
      setStep('extended');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId: string, answer: any) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      submitQuiz();
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const submitQuiz = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const answerArray: Answer[] = Object.entries(answers).map(([question_id, answer]) => ({
        question_id,
        answer
      }));

      if (step === 'initial') {
        const data = await submitInitialQuiz({ answers: answerArray });
        setProfileId(data.profile_id);
        setMatches(data.matches);
        setMatchType(data.match_type);
        setStep('results');
      } else if (step === 'extended' && profileId) {
        const data = await submitExtendedQuiz({ 
          profile_id: profileId,
          answers: answerArray 
        });
        setMatches(data.matches);
        setMatchType(data.match_type);
        setStep('program-results');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitFeedback = async () => {
    if (!profileId || rating === 0 || helpful === null) {
      setError('Please complete all feedback fields');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await submitFeedback({
        profile_id: profileId,
        rating,
        helpful,
        comments
      });

      alert('Thank you for your feedback!');
      // Reset to start
      setStep('initial');
      setCurrentQuestionIndex(0);
      setAnswers({});
      setMatches([]);
      setProfileId(null);
      setRating(0);
      setHelpful(null);
      setComments('');
      fetchInitialQuestions();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const renderQuestion = (question: Question) => {
    const currentAnswer = answers[question.id];

    switch (question.type) {
      case 'choice':
        return (
          <div className="question-options">
            {question.options?.map(option => (
              <button
                key={option}
                className={`option-button ${currentAnswer === option ? 'selected' : ''}`}
                onClick={() => handleAnswer(question.id, option)}
              >
                <div className="option-label">{option.replace(/_/g, ' ').toUpperCase()}</div>
                {question.descriptions && (
                  <div className="option-description">{question.descriptions[option]}</div>
                )}
              </button>
            ))}
          </div>
        );

      case 'multiple_choice':
        return (
          <div className="question-options multiple">
            {question.options?.map(option => {
              const selected = Array.isArray(currentAnswer) && currentAnswer.includes(option);
              return (
                <button
                  key={option}
                  className={`option-button ${selected ? 'selected' : ''}`}
                  onClick={() => {
                    const current = Array.isArray(currentAnswer) ? currentAnswer : [];
                    const updated = selected
                      ? current.filter(v => v !== option)
                      : [...current, option];
                    handleAnswer(question.id, updated);
                  }}
                >
                  <div className="option-label">{option.replace(/_/g, ' ').toUpperCase()}</div>
                  {question.descriptions && (
                    <div className="option-description">{question.descriptions[option]}</div>
                  )}
                </button>
              );
            })}
          </div>
        );

      case 'number':
        return (
          <input
            type="number"
            className="number-input"
            value={currentAnswer || ''}
            onChange={(e) => handleAnswer(question.id, parseFloat(e.target.value))}
            min={question.min}
            max={question.max}
            step={question.step}
          />
        );

      case 'range':
        return (
          <div className="range-input">
            <input
              type="range"
              value={currentAnswer || question.min || 0}
              onChange={(e) => handleAnswer(question.id, parseInt(e.target.value))}
              min={question.min}
              max={question.max}
              step={question.step}
            />
            <span className="range-value">{currentAnswer || question.min || 0}</span>
          </div>
        );

      case 'text':
      default:
        return (
          <input
            type="text"
            className="text-input"
            value={currentAnswer || ''}
            onChange={(e) => handleAnswer(question.id, e.target.value)}
            placeholder="Type your answer..."
          />
        );
    }
  };

  const renderMatches = () => {
    if (matches.length === 0) return <p>No matches found.</p>;

    const safety = matches.filter(m => m.match_type === 'safety');
    const target = matches.filter(m => m.match_type === 'target');
    const reach = matches.filter(m => m.match_type === 'reach');

    const renderMatchCard = (match: Match) => {
      const isProgram = 'program_name' in match;
      
      return (
        <div 
          key={isProgram ? (match as ProgramMatch).program_id : (match as UniversityMatch).university_name} 
          className="match-card"
        >
          <div className="match-header">
            <h3>{isProgram ? (match as ProgramMatch).program_name : (match as UniversityMatch).university_name}</h3>
            <span className={`match-badge ${match.match_type}`}>
              {match.match_type.toUpperCase()}
            </span>
          </div>
          
          <div className="match-score">
            <div className="score-circle">{match.match_score.toFixed(0)}</div>
            <span>Match Score</span>
          </div>

          {isProgram ? (
            <>
              <p><strong>🏫 University:</strong> {(match as ProgramMatch).university_name}</p>
              <p><strong>📍 Location:</strong> {(match as ProgramMatch).university_location}</p>
              <p><strong>🎓 Degree:</strong> {(match as ProgramMatch).degree_level.toUpperCase()} ({(match as ProgramMatch).duration_years} years)</p>
              <p><strong>🗣️ Language:</strong> {(match as ProgramMatch).language}</p>
              <p><strong>💰 Tuition:</strong> €{match.tuition_annual.toLocaleString()}/year</p>
              {(match as ProgramMatch).strength_rating && (
                <p><strong>⭐ Rating:</strong> {(match as ProgramMatch).strength_rating}/10</p>
              )}
            </>
          ) : (
            <>
              <p><strong>📍 Location:</strong> {(match as UniversityMatch).location}</p>
              <p><strong>💰 Tuition:</strong> €{match.tuition_annual.toLocaleString()}/year</p>
              <p><strong>📊 Acceptance Rate:</strong> {((match as UniversityMatch).acceptance_rate * 100).toFixed(0)}%</p>
              <p><strong>📏 Size:</strong> {(match as UniversityMatch).size}</p>
              <p><strong>💪 Strong Programs:</strong> {(match as UniversityMatch).strong_programs.join(', ')}</p>
            </>
          )}
          
          <div className="match-reasoning">
            <strong>Why this match:</strong>
            <p>{match.reasoning}</p>
          </div>
        </div>
      );
    };

    return (
      <div className="matches-container">
        {safety.length > 0 && (
          <div className="match-group">
            <h2 className="match-group-title safety">🟢 Safety {matchType === 'program' ? 'Programs' : 'Schools'}</h2>
            <div className="match-grid">{safety.map(renderMatchCard)}</div>
          </div>
        )}

        {target.length > 0 && (
          <div className="match-group">
            <h2 className="match-group-title target">🟡 Target {matchType === 'program' ? 'Programs' : 'Schools'}</h2>
            <div className="match-grid">{target.map(renderMatchCard)}</div>
          </div>
        )}

        {reach.length > 0 && (
          <div className="match-group">
            <h2 className="match-group-title reach">🔴 Reach {matchType === 'program' ? 'Programs' : 'Schools'}</h2>
            <div className="match-grid">{reach.map(renderMatchCard)}</div>
          </div>
        )}

        <div className="strategy-box">
          <h3>💡 Application Strategy</h3>
          <ul>
            <li>Apply to {safety.length} safety {matchType === 'program' ? 'program(s)' : 'school(s)'}</li>
            <li>Apply to {target.length} target {matchType === 'program' ? 'program(s)' : 'school(s)'}</li>
            <li>Apply to {reach.length} reach {matchType === 'program' ? 'program(s)' : 'school(s)'}</li>
          </ul>
        </div>
      </div>
    );
  };

  // Main render
  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="quiz-container">
          <div className="loading">Loading...</div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="quiz-container">
          <div className="error">
            <h2>Error</h2>
            <p>{error}</p>
            <button onClick={() => window.location.reload()}>Retry</button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Question screen
  if ((step === 'initial' || step === 'extended') && questions.length > 0) {
    const currentQuestion = questions[currentQuestionIndex];
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="quiz-container">
          <div className="quiz-header">
            <h1>🎓 UniHub - {step === 'initial' ? 'Initial Quiz' : 'Extended Quiz'}</h1>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }} />
            </div>
            <p className="progress-text">
              Question {currentQuestionIndex + 1} of {questions.length}
            </p>
          </div>

          <div className="question-container">
            <h2 className="question-text">{currentQuestion.question}</h2>
            {renderQuestion(currentQuestion)}
          </div>

          <div className="navigation-buttons">
            <button
              className="nav-button secondary"
              onClick={handlePrevious}
              disabled={currentQuestionIndex === 0}
            >
              ← Previous
            </button>
            <button
              className="nav-button primary"
              onClick={handleNext}
              disabled={!answers[currentQuestion.id]}
            >
              {currentQuestionIndex === questions.length - 1 ? 'Submit' : 'Next →'}
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Results screen
  if (step === 'results') {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="quiz-container">
          <div className="results-header">
            <h1>🎯 Your University Matches</h1>
            <p>Based on your profile, here are your personalized recommendations:</p>
          </div>

          {renderMatches()}

          <div className="results-actions">
            <button
              className="action-button primary"
              onClick={() => profileId && fetchExtendedQuestions(profileId)}
            >
              📚 Take Extended Quiz for Program Recommendations
            </button>
            <button
              className="action-button secondary"
              onClick={() => setStep('feedback')}
            >
              ✍️ Provide Feedback
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Program results screen
  if (step === 'program-results') {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="quiz-container">
          <div className="results-header">
            <h1>🎯 Your Program Matches</h1>
            <p>Based on your detailed profile, here are specific program recommendations:</p>
          </div>

          {renderMatches()}

          <div className="results-actions">
            <button
              className="action-button primary"
              onClick={() => setStep('feedback')}
            >
              ✍️ Provide Feedback
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Feedback screen
  if (step === 'feedback') {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="quiz-container">
          <div className="feedback-container">
            <h1>📝 Your Feedback</h1>
            <p>Help us improve your experience</p>

            <div className="feedback-section">
              <label>How would you rate our recommendations?</label>
              <div className="star-rating">
                {[1, 2, 3, 4, 5].map(star => (
                  <button
                    key={star}
                    className={`star ${rating >= star ? 'filled' : ''}`}
                    onClick={() => setRating(star)}
                  >
                    ★
                  </button>
                ))}
              </div>
            </div>

            <div className="feedback-section">
              <label>Were these recommendations helpful?</label>
              <div className="yes-no-buttons">
                <button
                  className={`yes-no-button ${helpful === true ? 'selected' : ''}`}
                  onClick={() => setHelpful(true)}
                >
                  👍 Yes
                </button>
                <button
                  className={`yes-no-button ${helpful === false ? 'selected' : ''}`}
                  onClick={() => setHelpful(false)}
                >
                  👎 No
                </button>
              </div>
            </div>

            <div className="feedback-section">
              <label>Additional comments (optional)</label>
              <textarea
                className="feedback-textarea"
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                placeholder="Tell us more about your experience..."
                rows={4}
              />
            </div>

            <button
              className="action-button primary"
              onClick={handleSubmitFeedback}
              disabled={rating === 0 || helpful === null}
            >
              Submit Feedback
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return null;
}
