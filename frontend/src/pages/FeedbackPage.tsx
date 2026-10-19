import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ScoreSummary } from '../components/ScoreSummary';
import { FeedbackPanel } from '../components/FeedbackPanel';
import { Attempt, FeedbackRecord } from '../types';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';
import { Sparkles, ArrowRight } from 'lucide-react';

export const FeedbackPage: React.FC = () => {
  const { id: attemptId } = useParams<{ id: string }>();
  const [attempt, setAttempt] = useState<Attempt | null>(null);
  const [feedback, setFeedback] = useState<FeedbackRecord | null>(null);
  const [recommendedLessonId, setRecommendedLessonId] = useState<string | null>(null);
  const [loadingFeedback, setLoadingFeedback] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { t } = useLanguage();

  useEffect(() => {
    async function init() {
      if (!attemptId) return;
      try {
        // 1. Fetch attempt data (contains instant score and rubric)
        const attData = await api.attempts.get(attemptId);
        setAttempt(attData);

        // 2. Fetch or trigger AI tutor feedback
        const fbData = await api.attempts.feedback(attemptId);
        setFeedback(fbData);

        // Map misconception to recommended lesson
        if (attData.misconception_tags && attData.misconception_tags.length > 0) {
          if (attData.misconception_tags.includes('MC-MACRO-MICRO-CONFUSED')) {
            setRecommendedLessonId('LESSON-MACRO-VS-MICRO');
          } else if (attData.misconception_tags.includes('MC-FERRITIN-MISSED') || attData.misconception_tags.includes('MC-DEFAULT-TO-IDA')) {
            setRecommendedLessonId('LESSON-FERRITIN-STORES');
          } else {
            setRecommendedLessonId('LESSON-MICROCYTIC-INDICES');
          }
        } else {
          setRecommendedLessonId('LESSON-MICROCYTIC-INDICES');
        }
      } catch (err: any) {
        setError(err.message || 'Error fetching evaluation and feedback');
      } finally {
        setLoadingFeedback(false);
      }
    }
    init();
  }, [attemptId]);

  const handleProceedLesson = () => {
    if (!attempt) return;
    const lessonId = recommendedLessonId || 'LESSON-MICROCYTIC-INDICES';
    navigate(`/lesson/${lessonId}?attemptId=${attempt.id}`);
  };

  const handleProceedReassess = async () => {
    if (!attempt) return;
    try {
      const res = await api.attempts.reassess(attempt.id);
      navigate(`/attempt/${res.attempt_id}`);
    } catch (err: any) {
      alert(`Could not start reassessment: ${err.message}`);
    }
  };

  if (!attempt && loadingFeedback) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Calculating rubric criteria and loading feedback...</span>
      </div>
    );
  }

  if (error || !attempt) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error || 'Attempt not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div>
        <span className="text-xs font-mono font-bold text-medblue-600 uppercase tracking-wider block">
          Evaluation Report · {attempt.case_id}
        </span>
        <h1 className="text-2xl font-black text-slate-900 tracking-tight">
          Clinical Reasoning Performance & Grounded Feedback
        </h1>
      </div>

      {/* Immediate Score & Rubric Checklist */}
      <ScoreSummary
        score={attempt.score || 0}
        maxScore={attempt.max_score || 10}
        isCorrect={attempt.is_correct}
        criteria={attempt.criteria_results}
      />

      {/* Grounded AI Tutor Feedback Panel or Skeleton Loader */}
      {loadingFeedback ? (
        <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-xs text-center space-y-3">
          <div className="w-10 h-10 rounded-xl bg-medblue-50 border border-medblue-200 text-medblue-600 flex items-center justify-center mx-auto animate-pulse">
            <Sparkles className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-slate-900">
            Grounding AI Feedback in Clinical Practice Guidelines...
          </h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto leading-relaxed">
            Retrieving approved guideline chunks, verifying citations, and evaluating reasoning gaps against British Society of Haematology criteria.
          </p>
          <div className="max-w-sm mx-auto pt-2 space-y-2">
            <div className="h-3 bg-slate-100 rounded-full animate-pulse" />
            <div className="h-3 bg-slate-100 rounded-full w-4/5 mx-auto animate-pulse" />
          </div>
        </div>
      ) : feedback ? (
        <FeedbackPanel
          feedback={feedback}
          onProceedLesson={handleProceedLesson}
          onProceedReassess={handleProceedReassess}
          recommendedLessonId={recommendedLessonId}
        />
      ) : null}
    </div>
  );
};
