import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { BookOpen, CheckCircle2, AlertCircle, ArrowRight, Sparkles, HelpCircle } from 'lucide-react';
import { Lesson, PracticeQuestion } from '../types';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export const LessonPage: React.FC = () => {
  const { id: lessonId } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const attemptId = searchParams.get('attemptId');

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [submittedAnswers, setSubmittedAnswers] = useState<Record<string, boolean>>({});
  const [completed, setCompleted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { t } = useLanguage();

  useEffect(() => {
    async function loadLesson() {
      if (!lessonId) return;
      try {
        const data = await api.lessons.get(lessonId);
        setLesson(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load lesson module');
      } finally {
        setLoading(false);
      }
    }
    loadLesson();
  }, [lessonId]);

  const handleSelectAnswer = (qId: string, optId: string) => {
    setSelectedAnswers((prev) => ({ ...prev, [qId]: optId }));
  };

  const handleCheckAnswer = (q: PracticeQuestion) => {
    const chosen = selectedAnswers[q.id];
    if (!chosen) return;
    const correctOpt = q.options.find((o) => o.correct);
    const isCorrect = correctOpt ? correctOpt.id === chosen : false;
    setSubmittedAnswers((prev) => ({ ...prev, [q.id]: isCorrect }));
  };

  const handleCompleteAndReassess = async () => {
    if (attemptId) {
      try {
        await api.attempts.lessonComplete(attemptId, selectedAnswers);
        const res = await api.attempts.reassess(attemptId);
        navigate(`/attempt/${res.attempt_id}`);
      } catch (err: any) {
        alert(`Could not start reassessment: ${err.message}`);
      }
    } else {
      navigate('/cases');
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Loading targeted clinical lesson...</span>
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error || 'Lesson not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div>
        <span className="text-xs font-mono font-bold text-medblue-600 uppercase tracking-wider block">
          Targeted Misconception-to-Mastery Module
        </span>
        <h1 className="text-2xl font-black text-slate-900 tracking-tight">
          {lesson.title}
        </h1>
      </div>

      {/* Clinical Overview */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-medblue-600" />
          <span>{t.lesson.overview}</span>
        </h3>
        <p className="text-sm text-slate-700 leading-relaxed font-normal">
          {lesson.content.overview}
        </p>

        {/* Key Principles */}
        <div className="pt-2 space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            {t.lesson.keyPrinciples}
          </h4>
          <div className="grid grid-cols-1 gap-3">
            {lesson.content.key_principles?.map((kp, idx) => (
              <div key={idx} className="bg-slate-50 border border-slate-200 rounded-lg p-3.5">
                <span className="text-xs font-bold text-slate-900 block mb-1">
                  {kp.title}
                </span>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {kp.explanation}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Clinical Practice Pearl */}
        {lesson.content.clinical_pearl && (
          <div className="bg-amber-50/70 border border-amber-200 rounded-lg p-4 flex items-start gap-2.5">
            <Sparkles className="w-4 h-4 text-amber-600 mt-0.5 shrink-0" />
            <div className="text-xs text-amber-900 leading-relaxed">
              <strong className="font-bold text-amber-950 block mb-0.5">
                {t.lesson.pearl}:
              </strong>
              {lesson.content.clinical_pearl}
            </div>
          </div>
        )}
      </div>

      {/* Formative Practice Quiz */}
      {lesson.practice_questions && lesson.practice_questions.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-6">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <HelpCircle className="w-4 h-4 text-medblue-600" />
            <span>{t.lesson.quizTitle}</span>
          </h3>

          <div className="space-y-6">
            {lesson.practice_questions.map((pq, qIdx) => {
              const selectedOpt = selectedAnswers[pq.id];
              const isChecked = submittedAnswers[pq.id] !== undefined;
              const isCorrect = submittedAnswers[pq.id];

              return (
                <div key={pq.id} className="border-t border-slate-100 pt-4 space-y-3">
                  <p className="text-sm font-bold text-slate-800">
                    {qIdx + 1}. {pq.question}
                  </p>

                  <div className="space-y-2">
                    {pq.options.map((opt) => {
                      const isChosen = selectedOpt === opt.id;
                      return (
                        <label
                          key={opt.id}
                          className={`flex items-start gap-2.5 p-3 rounded-lg border text-xs cursor-pointer transition-colors ${
                            isChosen
                              ? 'bg-medblue-50 border-medblue-400 font-semibold text-slate-900'
                              : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700'
                          }`}
                        >
                          <input
                            type="radio"
                            name={`quiz_${pq.id}`}
                            value={opt.id}
                            checked={isChosen}
                            onChange={() => handleSelectAnswer(pq.id, opt.id)}
                            className="mt-0.5 text-medblue-600 focus:ring-medblue-500"
                          />
                          <span>
                            <strong>{opt.id}.</strong> {opt.text}
                          </span>
                        </label>
                      );
                    })}
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <button
                      type="button"
                      onClick={() => handleCheckAnswer(pq)}
                      disabled={!selectedOpt}
                      className="px-3 py-1.5 rounded-lg text-xs font-bold text-medblue-700 bg-medblue-50 hover:bg-medblue-100 border border-medblue-200 transition-colors disabled:opacity-50"
                    >
                      {t.lesson.checkAnswer}
                    </button>

                    {isChecked && (
                      <div className="flex items-center gap-1.5 text-xs font-bold">
                        {isCorrect ? (
                          <span className="text-emerald-600 flex items-center gap-1">
                            <CheckCircle2 className="w-4 h-4" /> Correct reasoning!
                          </span>
                        ) : (
                          <span className="text-rose-600 flex items-center gap-1">
                            <AlertCircle className="w-4 h-4" /> Review the clinical pearl
                          </span>
                        )}
                      </div>
                    )}
                  </div>

                  {isChecked && pq.explanation && (
                    <div className="text-xs bg-slate-50 p-3 rounded-lg border border-slate-200 text-slate-600">
                      <strong>Explanation:</strong> {pq.explanation}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Complete Button to proceed to Reassessment */}
      <div className="pt-2">
        <button
          onClick={handleCompleteAndReassess}
          className="w-full py-3.5 px-6 rounded-xl font-bold text-white bg-teal-600 hover:bg-teal-700 shadow-md shadow-teal-600/20 transition-all flex items-center justify-center gap-2 text-sm"
        >
          <span>{t.lesson.completeBtn}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
