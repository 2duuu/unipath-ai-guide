// Example: Integration with React Router (App.tsx)
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Quiz from './pages/Quiz';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz" element={<Quiz />} />
      </Routes>
    </Router>
  );
}

export default App;

// ============================================

// Example: Integration with Next.js (pages/quiz.tsx or app/quiz/page.tsx)

// For Next.js Pages Router:
// Create file: pages/quiz.tsx
import Quiz from '../components/Quiz';

export default function QuizPage() {
  return <Quiz />;
}

// For Next.js App Router:
// Create file: app/quiz/page.tsx
'use client'; // Required for client-side interactivity

import Quiz from '@/components/Quiz';

export default function QuizPage() {
  return <Quiz />;
}

// ============================================

// Example: Using the API Client (recommended approach)
import { UniHubAPI } from './types';
import { useState, useEffect } from 'react';

function QuizWithAPI() {
  const [api] = useState(() => new UniHubAPI('http://localhost:8000'));
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await api.getInitialQuestions();
      setQuestions(data.questions);
    } catch (error) {
      console.error('Failed to load questions:', error);
    }
  };

  const handleSubmit = async (answers) => {
    try {
      const result = await api.submitInitialQuiz(answers);
      console.log('Matches:', result.matches);
    } catch (error) {
      console.error('Failed to submit:', error);
    }
  };

  // ... rest of your component
}

// ============================================

// Example: Environment-based API URL
// .env.development
// REACT_APP_API_URL=http://localhost:8000

// .env.production
// REACT_APP_API_URL=https://api.unihub.com

// In Quiz.tsx, update:
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// For Next.js:
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// For Vite:
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
