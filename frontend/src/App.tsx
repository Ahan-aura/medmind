import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LanguageProvider } from './i18n/LanguageContext';
import { DisclaimerBanner } from './components/DisclaimerBanner';
import { DemoWalkthroughBar } from './components/DemoWalkthroughBar';
import { Navbar } from './components/Navbar';

import { LoginPage } from './pages/LoginPage';
import { CaseListPage } from './pages/CaseListPage';
import { CasePlayerPage } from './pages/CasePlayerPage';
import { FeedbackPage } from './pages/FeedbackPage';
import { LessonPage } from './pages/LessonPage';
import { ComparePage } from './pages/ComparePage';
import { ProgressPage } from './pages/ProgressPage';
import { TeacherPage } from './pages/TeacherPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode; requireTeacher?: boolean }> = ({
  children,
  requireTeacher = false,
}) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requireTeacher && user.role !== 'teacher' && user.role !== 'admin') {
    return <Navigate to="/cases" replace />;
  }

  return <>{children}</>;
};

export const AppContent: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <DisclaimerBanner />
      <DemoWalkthroughBar />
      <Navbar />

      <main className="flex-1">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/cases"
            element={
              <ProtectedRoute>
                <CaseListPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/attempt/:id"
            element={
              <ProtectedRoute>
                <CasePlayerPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/attempt/:id/feedback"
            element={
              <ProtectedRoute>
                <FeedbackPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/lesson/:id"
            element={
              <ProtectedRoute>
                <LessonPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/attempt/:id/compare"
            element={
              <ProtectedRoute>
                <ComparePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/progress"
            element={
              <ProtectedRoute>
                <ProgressPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/teacher"
            element={
              <ProtectedRoute requireTeacher>
                <TeacherPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/cases" replace />} />
        </Routes>
      </main>

      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 space-y-1">
          <p className="font-semibold text-slate-700">
            MEDMIND AI 2.0 (YUKTHI 26) · Clinical Reasoning Simulation & Assessment Platform
          </p>
          <p className="text-slate-400">
            Deterministic Evaluation Engine + Evidence-Grounded AI Tutor · Built for Medical and Nursing Education
          </p>
        </div>
      </footer>
    </div>
  );
};

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppContent />
        </BrowserRouter>
      </AuthProvider>
    </LanguageProvider>
  );
}
