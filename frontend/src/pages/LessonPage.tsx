import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate, Link } from 'react-router-dom';
import {
  BookOpen,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Sparkles,
  HelpCircle,
  Clock,
  ExternalLink,
  X,
  AlertTriangle,
  Lightbulb,
  Award,
  ChevronLeft,
  ChevronDown,
  ChevronUp,
  FileText
} from 'lucide-react';
import { LessonDetail, QuickCheckQuestion, ReferenceSummary, QuizResult } from '../types';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export const LessonPage: React.FC = () => {
  const { id: lessonId } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const attemptId = searchParams.get('attemptId');

  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [quizSubmitting, setQuizSubmitting] = useState(false);
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);
  const [quizError, setQuizError] = useState<string | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Stepped/collapsible state for worked example
  const [showAllSteps, setShowAllSteps] = useState(true);

  // Modal for reference passage popover
  const [activeReference, setActiveReference] = useState<ReferenceSummary | null>(null);

  const navigate = useNavigate();
  const { language, t } = useLanguage();

  useEffect(() => {
    async function loadLesson() {
      if (!lessonId) return;
      try {
        setLoading(true);
        const data = await api.lessons.get(lessonId);
        setLesson(data);
        // Reset quiz state when switching lessons
        setSelectedAnswers({});
        setQuizResult(null);
        setQuizError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to load lesson module');
      } finally {
        setLoading(false);
      }
    }
    loadLesson();
  }, [lessonId]);

  const handleSelectAnswer = (qId: string, optId: string) => {
    if (quizResult) return; // Disabled after submit
    setSelectedAnswers((prev) => ({ ...prev, [qId]: optId }));
  };

  const handleSubmitQuiz = async () => {
    if (!lesson || !lessonId) return;
    const questions = lesson.quick_check || [];
    
    // Check all questions answered
    const unanswered = questions.filter((q) => !selectedAnswers[q.id]);
    if (unanswered.length > 0) {
      setQuizError('Please select an answer for all 3 questions before submitting.');
      return;
    }

    try {
      setQuizSubmitting(true);
      setQuizError(null);
      const res = await api.lessons.submitQuiz(lessonId, selectedAnswers);
      setQuizResult(res);

      // If attemptId is present, also notify attempt module
      if (attemptId) {
        try {
          await api.attempts.lessonComplete(attemptId, selectedAnswers);
        } catch {
          // non-fatal
        }
      }
    } catch (err: any) {
      setQuizError(err.message || 'Failed to submit quiz. Please try again.');
    } finally {
      setQuizSubmitting(false);
    }
  };

  const handleReturnToReassessment = async () => {
    if (attemptId) {
      try {
        const res = await api.attempts.reassess(attemptId);
        navigate(`/attempt/${res.attempt_id}`);
      } catch (err: any) {
        alert(`Could not start reassessment: ${err.message}`);
      }
    } else {
      navigate('/cases');
    }
  };

  const openReferenceModal = (refId: string) => {
    if (!lesson) return;
    const refData = lesson.references?.[refId] || {
      id: refId,
      title: refId,
      source_title: 'Clinical Haematology Reference',
      source_url: 'https://b-s-h.org.uk',
      text: 'Detailed reference passage retrieved from curated clinical guidelines.',
      key_facts: []
    };
    setActiveReference(refData);
  };

  const getDifficultyBadge = (diff: number) => {
    switch (diff) {
      case 1:
        return (
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Level 1 · Fundamental
          </span>
        );
      case 2:
        return (
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            Level 2 · Intermediate
          </span>
        );
      case 3:
      default:
        return (
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            Level 3 · Advanced
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Loading clinical practice lesson...</span>
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4 space-y-4">
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error || 'Lesson not found'}
        </div>
        <Link
          to="/lessons"
          className="inline-flex items-center gap-1 text-sm font-semibold text-medblue-600 hover:text-medblue-800"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Return to Lesson Library</span>
        </Link>
      </div>
    );
  }

  const isComplete = quizResult?.passed ?? lesson.completed;
  const currentBestScore = quizResult ? quizResult.best_score : lesson.best_score;

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Telugu Translation In Progress Notice */}
      {language === 'te' && (
        <div className="p-3.5 rounded-xl bg-amber-50/80 border border-amber-200 text-amber-900 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            {(t as any).lessonsLibrary?.teluguProgressNotice ||
              'తెలుగు అనువాదం పురోగతిలో ఉంది — ఆంగ్ల సంస్కరణ చూపబడుతోంది. (Telugu translation in progress — displaying English version with clinical terms).'}
          </span>
        </div>
      )}

      {/* Breadcrumb Navigation */}
      <div className="flex items-center justify-between">
        <Link
          to="/lessons"
          className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-medblue-600 transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Back to Lesson Library</span>
        </Link>

        {attemptId && (
          <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-semibold bg-medblue-50 text-medblue-700 border border-medblue-200">
            Case Encounter Active: {attemptId.slice(0, 8)}
          </span>
        )}
      </div>

      {/* SECTION 1: HEADER */}
      <header className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 rounded-md text-xs font-mono font-bold uppercase tracking-wider bg-slate-100 text-slate-700">
              {lesson.id}
            </span>
            {lesson.objective_id && (
              <span className="px-2.5 py-1 rounded-md text-xs font-mono bg-medblue-50 text-medblue-700 border border-medblue-200">
                {lesson.objective_id}
              </span>
            )}
          </div>

          {/* Draft Badge with Tooltip */}
          <div
            title="This educational lesson is in draft form and has not yet completed formal clinical review. For simulation study only."
            className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-50 text-amber-800 border border-amber-300 flex items-center gap-1.5 cursor-help shadow-xs"
          >
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            <span>Draft - pending clinical review</span>
          </div>
        </div>

        <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight leading-tight">
          {lesson.title}
        </h1>

        <div className="flex flex-wrap items-center gap-3 pt-1 text-xs text-slate-500">
          <span className="flex items-center gap-1 font-semibold text-slate-700">
            <Clock className="w-4 h-4 text-slate-400" />
            {lesson.estimated_minutes} minutes
          </span>
          <span>•</span>
          {getDifficultyBadge(lesson.difficulty)}
          {currentBestScore !== undefined && currentBestScore !== null && (
            <>
              <span>•</span>
              <span className="font-semibold text-emerald-700 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Best Score: {currentBestScore}/3
              </span>
            </>
          )}
        </div>
      </header>

      {/* SECTION 2: LEARNING OUTCOMES */}
      {lesson.learning_outcomes && lesson.learning_outcomes.length > 0 && (
        <section className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-medblue-600" />
            <span>Learning Outcomes</span>
          </h2>
          <ul className="space-y-2.5">
            {lesson.learning_outcomes.map((outcome, idx) => (
              <li key={idx} className="flex items-start gap-3 text-sm text-slate-700">
                <div className="w-5 h-5 rounded-full bg-medblue-50 text-medblue-700 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5 border border-medblue-200">
                  {idx + 1}
                </div>
                <span className="leading-relaxed font-medium">{outcome}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* SECTION 3: KEY POINTS WITH CLICKABLE REFERENCE CHIPS */}
      {lesson.key_points && lesson.key_points.length > 0 && (
        <section className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-medblue-600" />
            <span>Core Key Points & Evidence Links</span>
          </h2>
          <div className="space-y-3">
            {lesson.key_points.map((kp, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl bg-slate-50/70 border border-slate-200/80 flex flex-col sm:flex-row sm:items-start justify-between gap-3"
              >
                <div className="flex items-start gap-2.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-medblue-600 mt-2 shrink-0" />
                  <p className="text-sm text-slate-800 leading-relaxed font-normal">
                    {kp.point}
                  </p>
                </div>

                {/* Reference Chips */}
                {kp.refs && kp.refs.length > 0 && (
                  <div className="flex flex-wrap items-center gap-1.5 shrink-0 self-end sm:self-auto pt-1 sm:pt-0">
                    {kp.refs.map((rId) => (
                      <button
                        key={rId}
                        onClick={() => openReferenceModal(rId)}
                        className="inline-flex items-center gap-1 text-[11px] font-mono font-bold px-2 py-0.5 rounded bg-medblue-50 text-medblue-700 border border-medblue-200 hover:bg-medblue-100 hover:border-medblue-300 transition-colors"
                        title="Click to view full reference passage"
                      >
                        <FileText className="w-3 h-3" />
                        <span>{rId}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SECTION 4: WORKED EXAMPLE (VIGNETTE & REASONING STEPS) */}
      {lesson.worked_example && (
        <section className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
              <Award className="w-4 h-4 text-medblue-600" />
              <span>Worked Clinical Example</span>
            </h2>
            {lesson.worked_example.steps && lesson.worked_example.steps.length > 0 && (
              <button
                onClick={() => setShowAllSteps(!showAllSteps)}
                className="text-xs font-semibold text-medblue-600 hover:text-medblue-800 flex items-center gap-1"
              >
                <span>{showAllSteps ? 'Collapse Reasoning' : 'Expand Reasoning'}</span>
                {showAllSteps ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>
            )}
          </div>

          {/* Vignette Card */}
          <div className="p-4 rounded-xl bg-slate-50 border-l-4 border-l-medblue-600 border border-slate-200 text-sm text-slate-700 leading-relaxed font-normal">
            <span className="font-bold text-slate-900 block mb-1">Fictional Patient Scenario:</span>
            {lesson.worked_example.vignette}
          </div>

          {/* Reasoning Steps */}
          {showAllSteps && lesson.worked_example.steps && (
            <div className="space-y-2 pt-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
                Step-by-Step Diagnostic Walk-Through:
              </span>
              <div className="space-y-2">
                {lesson.worked_example.steps.map((st, sIdx) => (
                  <div
                    key={sIdx}
                    className="p-3 rounded-lg bg-white border border-slate-200 text-xs text-slate-700 flex items-start gap-2.5 shadow-2xs"
                  >
                    <span className="w-5 h-5 rounded-full bg-slate-100 font-mono font-bold text-slate-600 text-[11px] flex items-center justify-center shrink-0">
                      {sIdx + 1}
                    </span>
                    <span className="leading-relaxed font-medium">{st}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      {/* SECTION 5: COMMON PITFALLS */}
      {lesson.common_pitfalls && lesson.common_pitfalls.length > 0 && (
        <section className="bg-rose-50/60 rounded-2xl border border-rose-200 p-6 shadow-xs space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-rose-900 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600" />
            <span>Common Diagnostic Pitfalls</span>
          </h2>
          <div className="space-y-2.5">
            {lesson.common_pitfalls.map((pitfall, pIdx) => (
              <div
                key={pIdx}
                className="p-3.5 rounded-xl bg-white border border-rose-200 text-sm text-rose-950 flex items-start gap-3 shadow-2xs"
              >
                <div className="w-5 h-5 rounded-full bg-rose-100 text-rose-700 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                  !
                </div>
                <p className="leading-relaxed font-normal">{pitfall}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SECTION 6: CLINICAL PEARL */}
      {lesson.clinical_pearl && (
        <section className="bg-gradient-to-r from-medblue-900 via-slate-900 to-medblue-950 rounded-2xl p-6 text-white shadow-md relative overflow-hidden">
          <div className="absolute right-4 top-4 text-medblue-500/20 pointer-events-none">
            <Lightbulb className="w-24 h-24 stroke-[1]" />
          </div>
          <div className="relative z-10 space-y-2 max-w-2xl">
            <span className="text-[11px] font-mono font-bold tracking-wider text-medblue-300 uppercase flex items-center gap-1.5">
              <Lightbulb className="w-4 h-4 text-amber-400 fill-amber-400" />
              Clinical Practice Pearl
            </span>
            <p className="text-base sm:text-lg font-semibold italic text-slate-100 leading-snug">
              "{lesson.clinical_pearl}"
            </p>
          </div>
        </section>
      )}

      {/* SECTION 7: QUICK CHECK (FORMATIVE ASSESSMENT QUIZ) */}
      {lesson.quick_check && lesson.quick_check.length > 0 && (
        <section className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <HelpCircle className="w-5 h-5 text-medblue-600" />
                <span>Quick Check (3 Practice Questions)</span>
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Test your interpretation and clinical reasoning. Answers are verified upon submission.
              </p>
            </div>
            {lesson.completed && !quizResult && (
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                Previously Passed ({lesson.best_score}/3)
              </span>
            )}
          </div>

          {quizError && (
            <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs">
              {quizError}
            </div>
          )}

          <div className="space-y-6">
            {lesson.quick_check.map((q, qIndex) => {
              const res = quizResult?.results?.[q.id];
              const chosen = selectedAnswers[q.id];

              return (
                <div key={q.id} className="p-5 rounded-xl bg-slate-50/70 border border-slate-200/90 space-y-4">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-start gap-2.5">
                      <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-slate-200 text-slate-700 shrink-0 mt-0.5">
                        Q{qIndex + 1}
                      </span>
                      <p className="text-sm font-bold text-slate-900 leading-snug">
                        {q.prompt}
                      </p>
                    </div>

                    {/* Result indicator badge if submitted */}
                    {res && (
                      <span
                        className={`px-2 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider shrink-0 ${
                          res.is_correct
                            ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                            : 'bg-rose-100 text-rose-800 border border-rose-300'
                        }`}
                      >
                        {res.is_correct ? 'Correct' : 'Incorrect'}
                      </span>
                    )}
                  </div>

                  {/* 4 Options */}
                  <div className="grid grid-cols-1 gap-2 pt-1">
                    {q.options.map((opt) => {
                      const isSelected = chosen === opt.id;
                      let optionStyle = 'bg-white border-slate-200 text-slate-700 hover:border-slate-300';

                      if (res) {
                        // Post-submission feedback styling
                        if (opt.id === res.correct) {
                          optionStyle = 'bg-emerald-50/90 border-emerald-500 text-emerald-900 font-semibold ring-1 ring-emerald-500';
                        } else if (isSelected && !res.is_correct) {
                          optionStyle = 'bg-rose-50/90 border-rose-500 text-rose-900 line-through';
                        } else {
                          optionStyle = 'bg-white border-slate-200 text-slate-400 opacity-60';
                        }
                      } else if (isSelected) {
                        optionStyle = 'bg-medblue-50 border-medblue-600 text-medblue-900 font-semibold ring-1 ring-medblue-600';
                      }

                      return (
                        <button
                          key={opt.id}
                          type="button"
                          disabled={!!quizResult || quizSubmitting}
                          onClick={() => handleSelectAnswer(q.id, opt.id)}
                          className={`w-full text-left p-3.5 rounded-xl border text-sm transition-all flex items-start gap-3 ${optionStyle}`}
                        >
                          <span
                            className={`w-6 h-6 rounded-lg font-mono font-bold text-xs flex items-center justify-center shrink-0 mt-0.5 ${
                              isSelected
                                ? 'bg-medblue-600 text-white'
                                : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            {opt.id}
                          </span>
                          <span className="leading-relaxed">{opt.text}</span>
                        </button>
                      );
                    })}
                  </div>

                  {/* Immediate Rationale Display after Quiz Submit */}
                  {res && (
                    <div
                      className={`p-4 rounded-xl border text-xs leading-relaxed space-y-1.5 ${
                        res.is_correct
                          ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900'
                          : 'bg-amber-50/60 border-amber-200 text-amber-950'
                      }`}
                    >
                      <div className="flex items-center justify-between font-bold">
                        <span>Clinical Rationale:</span>
                        {res.reference_id && (
                          <button
                            onClick={() => openReferenceModal(res.reference_id!)}
                            className="text-[11px] font-mono text-medblue-700 underline hover:text-medblue-900"
                          >
                            View Evidence [{res.reference_id}]
                          </button>
                        )}
                      </div>
                      <p>{res.rationale}</p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Submit Quiz Button */}
          {!quizResult && (
            <div className="pt-2 flex justify-end">
              <button
                type="button"
                disabled={quizSubmitting || Object.keys(selectedAnswers).length < (lesson.quick_check?.length || 3)}
                onClick={handleSubmitQuiz}
                className="px-6 py-2.5 rounded-xl bg-medblue-600 hover:bg-medblue-700 text-white text-sm font-bold shadow-md shadow-medblue-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {quizSubmitting ? 'Scoring Answers...' : 'Submit Quick Check'}
              </button>
            </div>
          )}
        </section>
      )}

      {/* SECTION 8: RESULT SUMMARY */}
      {quizResult && (
        <section
          className={`rounded-2xl border p-6 sm:p-8 shadow-sm space-y-4 ${
            quizResult.passed
              ? 'bg-gradient-to-br from-emerald-500/10 via-emerald-50/40 to-teal-50/30 border-emerald-300'
              : 'bg-gradient-to-br from-amber-500/10 via-amber-50/40 to-orange-50/30 border-amber-300'
          }`}
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500">
                Module Performance Summary
              </span>
              <h3 className="text-2xl font-black text-slate-900 flex items-center gap-2">
                <span>Score: {quizResult.score} / {quizResult.max_score}</span>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                    quizResult.passed
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'bg-amber-600 text-white shadow-xs'
                  }`}
                >
                  {quizResult.passed ? 'Passed · Concept Mastered' : 'Try Again (Passing is 2/3)'}
                </span>
              </h3>
              <p className="text-xs text-slate-600">
                {quizResult.passed
                  ? 'Congratulations! You demonstrated sound interpretation of these diagnostic haematology principles.'
                  : 'Review the rationale feedback above and try again to consolidate your reasoning.'}
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-3">
              {attemptId ? (
                <button
                  type="button"
                  onClick={handleReturnToReassessment}
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all"
                >
                  <span>Proceed to Reassessment Case</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <Link
                  to="/lessons"
                  className="px-5 py-2.5 rounded-xl bg-medblue-600 hover:bg-medblue-700 text-white text-sm font-bold shadow-md shadow-medblue-500/20 flex items-center gap-2 transition-all"
                >
                  <span>Return to Lesson Library</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              )}
            </div>
          </div>
        </section>
      )}

      {/* Further Reading Section */}
      {lesson.further_reading && lesson.further_reading.length > 0 && (
        <section className="bg-slate-50 rounded-2xl border border-slate-200 p-6 text-xs text-slate-600 space-y-3">
          <span className="font-bold text-slate-800 uppercase tracking-wider block">
            Authoritative Guidelines & Further Reading
          </span>
          <ul className="space-y-1.5">
            {lesson.further_reading.map((fr, idx) => (
              <li key={idx} className="flex items-center gap-2">
                <ExternalLink className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                {fr.url ? (
                  <a
                    href={fr.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium text-medblue-700 hover:underline"
                  >
                    {fr.title}
                  </a>
                ) : (
                  <span>{fr.title}</span>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Reference Popover / Modal */}
      {activeReference && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full border border-slate-200 shadow-2xl p-6 sm:p-8 space-y-4 max-h-[85vh] overflow-y-auto animate-in fade-in zoom-in duration-150">
            <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-3">
              <div>
                <span className="text-[11px] font-mono font-bold text-medblue-700 bg-medblue-50 px-2 py-0.5 rounded border border-medblue-200">
                  {activeReference.id}
                </span>
                <h3 className="text-lg font-bold text-slate-900 mt-1">
                  {activeReference.title || activeReference.source_title}
                </h3>
              </div>
              <button
                onClick={() => setActiveReference(null)}
                className="w-8 h-8 rounded-lg bg-slate-100 text-slate-500 hover:bg-slate-200 flex items-center justify-center transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Source Title & Link */}
            <div className="text-xs text-slate-500 space-y-1">
              <p>
                <strong className="text-slate-700">Source:</strong> {activeReference.source_title}
              </p>
              {activeReference.source_url && (
                <p>
                  <a
                    href={activeReference.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-medblue-600 hover:underline inline-flex items-center gap-1 font-semibold"
                  >
                    <span>View Public Guideline Document</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </p>
              )}
            </div>

            {/* Key Facts */}
            {activeReference.key_facts && activeReference.key_facts.length > 0 && (
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 space-y-1">
                <span className="font-bold text-slate-900 block">Guideline Key Facts:</span>
                <ul className="list-disc pl-4 space-y-0.5">
                  {activeReference.key_facts.map((fact, fIdx) => (
                    <li key={fIdx}>{fact}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Reference Passage Body */}
            <div className="text-sm text-slate-800 leading-relaxed space-y-3 pt-2">
              <p>{activeReference.text}</p>
            </div>

            {/* Footer */}
            <div className="pt-4 border-t border-slate-100 flex justify-end">
              <button
                onClick={() => setActiveReference(null)}
                className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-colors"
              >
                Close Reference
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
