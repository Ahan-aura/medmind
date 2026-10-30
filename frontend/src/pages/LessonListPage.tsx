import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  GraduationCap,
  Sparkles,
  Clock,
  CheckCircle2,
  AlertTriangle,
  ChevronRight,
  BookOpen,
  HelpCircle,
  Filter,
  Flame
} from 'lucide-react';
import { api } from '../api/client';
import { LessonListItem } from '../types';
import { useLanguage } from '../i18n/LanguageContext';

export const LessonListPage: React.FC = () => {
  const [lessons, setLessons] = useState<LessonListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState<number | 'all'>('all');
  const { t } = useLanguage();

  useEffect(() => {
    async function loadLessons() {
      try {
        const data = await api.lessons.list();
        setLessons(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load lesson modules');
      } finally {
        setLoading(false);
      }
    }
    loadLessons();
  }, []);

  const recommendedLessons = lessons.filter((l) => l.recommended);
  const filteredLessons = lessons.filter((l) => {
    if (selectedDifficulty === 'all') return true;
    return l.difficulty === selectedDifficulty;
  });

  const getDifficultyBadge = (diff: number) => {
    switch (diff) {
      case 1:
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Level 1 · Fundamental
          </span>
        );
      case 2:
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            Level 2 · Intermediate
          </span>
        );
      case 3:
      default:
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            Level 3 · Advanced
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Loading clinical practice lessons...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto py-12 px-4">
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider bg-medblue-50 text-medblue-700 border border-medblue-200 flex items-center gap-1.5">
            <GraduationCap className="w-3.5 h-3.5" />
            Curated Practice Curriculum
          </span>
        </div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">
          {(t as any).lessonsLibrary?.title || 'Doctor Practice Lessons'}
        </h1>
        <p className="text-sm text-slate-600 mt-1 max-w-3xl">
          {(t as any).lessonsLibrary?.subtitle ||
            'Targeted clinical reasoning modules grounded in haematology evidence and guidelines. Work through systematic interpretation, diagnostic heuristics, and safety escalation.'}
        </p>
      </div>

      {/* Prominent Recommended for You Section */}
      {recommendedLessons.length > 0 && (
        <section className="bg-gradient-to-br from-amber-500/10 via-amber-50/50 to-orange-50/40 rounded-2xl border-2 border-amber-300 p-6 space-y-4 shadow-sm">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-amber-500 text-white flex items-center justify-center shadow-sm">
                <Flame className="w-5 h-5 fill-white" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <span>{(t as any).lessonsLibrary?.recommendedTitle || 'Recommended for You'}</span>
                  <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-200 text-amber-900">
                    High Priority
                  </span>
                </h2>
                <p className="text-xs text-slate-600">
                  {(t as any).lessonsLibrary?.recommendedSubtitle ||
                    'Targeted lessons triggered by recent diagnostic reasoning patterns or missed indices in simulator cases.'}
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendedLessons.map((lesson) => (
              <div
                key={lesson.id}
                className="bg-white rounded-xl border border-amber-200 p-5 shadow-xs hover:border-amber-400 hover:shadow-md transition-all flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded">
                      {lesson.id}
                    </span>
                    <span
                      title="This educational lesson is in draft form and has not yet completed formal clinical review. For simulation study only."
                      className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-800 border border-amber-300 flex items-center gap-1 cursor-help"
                    >
                      <AlertTriangle className="w-3 h-3 text-amber-600" />
                      Draft - pending review
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-slate-900 leading-snug">
                    {lesson.title}
                  </h3>

                  <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {lesson.estimated_minutes} mins
                    </span>
                    <span>•</span>
                    {getDifficultyBadge(lesson.difficulty)}
                  </div>

                  {lesson.targets_misconceptions && lesson.targets_misconceptions.length > 0 && (
                    <div className="flex flex-wrap gap-1 pt-1">
                      {lesson.targets_misconceptions.map((mc) => (
                        <span
                          key={mc}
                          className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-100 text-slate-600 border border-slate-200"
                        >
                          targets: {mc}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="pt-4 mt-2 border-t border-slate-100 flex items-center justify-between">
                  <div className="text-xs">
                    {lesson.completed ? (
                      <span className="text-emerald-700 font-semibold flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        Best: {lesson.best_score}/3
                      </span>
                    ) : (
                      <span className="text-slate-400 font-medium">Not started</span>
                    )}
                  </div>
                  <Link
                    to={`/lesson/${lesson.id}`}
                    className="inline-flex items-center gap-1 text-xs font-bold px-3 py-1.5 rounded-lg bg-medblue-600 text-white hover:bg-medblue-700 shadow-xs transition-colors"
                  >
                    <span>{lesson.completed ? 'Review Lesson' : 'Start Lesson'}</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Filter and Library Section */}
      <section className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-medblue-600" />
              <span>{(t as any).lessonsLibrary?.allLessonsTitle || 'All Practice Lessons'}</span>
              <span className="text-sm font-semibold text-slate-400">({lessons.length})</span>
            </h2>
          </div>

          {/* Difficulty filter tabs */}
          <div className="flex items-center gap-1 p-1 bg-slate-100 rounded-xl border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => setSelectedDifficulty('all')}
              className={`px-3 py-1 rounded-lg transition-all ${
                selectedDifficulty === 'all'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All Levels
            </button>
            <button
              onClick={() => setSelectedDifficulty(1)}
              className={`px-3 py-1 rounded-lg transition-all ${
                selectedDifficulty === 1
                  ? 'bg-emerald-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Level 1
            </button>
            <button
              onClick={() => setSelectedDifficulty(2)}
              className={`px-3 py-1 rounded-lg transition-all ${
                selectedDifficulty === 2
                  ? 'bg-amber-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Level 2
            </button>
            <button
              onClick={() => setSelectedDifficulty(3)}
              className={`px-3 py-1 rounded-lg transition-all ${
                selectedDifficulty === 3
                  ? 'bg-rose-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Level 3
            </button>
          </div>
        </div>

        {/* Lessons Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredLessons.map((lesson) => (
            <div
              key={lesson.id}
              className={`bg-white rounded-xl border transition-all duration-200 hover:shadow-md flex flex-col justify-between ${
                lesson.completed
                  ? 'border-emerald-200 shadow-xs ring-1 ring-emerald-500/10'
                  : 'border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="p-5 space-y-3">
                {/* Card Top Meta */}
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                    {lesson.id}
                  </span>
                  {/* Draft Badge with Tooltip */}
                  <span
                    title="This educational lesson is in draft form and has not yet completed formal clinical review. For simulation study only."
                    className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-50 text-amber-800 border border-amber-200 flex items-center gap-1 cursor-help"
                  >
                    <AlertTriangle className="w-3 h-3 text-amber-600" />
                    Draft - pending review
                  </span>
                </div>

                {/* Title */}
                <h3 className="text-base font-bold text-slate-900 leading-snug line-clamp-2">
                  {lesson.title}
                </h3>

                {/* Details */}
                <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {lesson.estimated_minutes} mins
                  </span>
                  <span>•</span>
                  {getDifficultyBadge(lesson.difficulty)}
                </div>

                {/* Misconception tags */}
                {lesson.targets_misconceptions && lesson.targets_misconceptions.length > 0 && (
                  <div className="flex flex-wrap gap-1 pt-1">
                    {lesson.targets_misconceptions.map((mc) => (
                      <span
                        key={mc}
                        className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-50 text-slate-600 border border-slate-200"
                      >
                        {mc}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Card Footer */}
              <div className="p-4 bg-slate-50/60 border-t border-slate-100 rounded-b-xl flex items-center justify-between">
                <div>
                  {lesson.completed ? (
                    <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-700">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      <span>Passed ({lesson.best_score}/3)</span>
                    </div>
                  ) : (
                    <span className="text-xs text-slate-400 font-medium">Uncompleted</span>
                  )}
                </div>

                <Link
                  to={`/lesson/${lesson.id}`}
                  className="inline-flex items-center gap-1 text-xs font-bold px-3 py-1.5 rounded-lg bg-medblue-600 text-white hover:bg-medblue-700 shadow-xs transition-colors"
                >
                  <span>{lesson.completed ? 'Review' : 'Start'}</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
