import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, ArrowRight, ShieldCheck, Tag, Stethoscope, RefreshCw } from 'lucide-react';
import { CaseListItem } from '../types';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export const CaseListPage: React.FC = () => {
  const [cases, setCases] = useState<CaseListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { t, language } = useLanguage();
  const navigate = useNavigate();

  useEffect(() => {
    async function loadCases() {
      try {
        const data = await api.cases.list();
        setCases(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load cases');
      } finally {
        setLoading(false);
      }
    }
    loadCases();
  }, []);

  const handleStartCase = async (caseId: string) => {
    try {
      const res = await api.attempts.start(caseId, language);
      navigate(`/attempt/${res.attempt_id}`);
    } catch (err: any) {
      alert(`Could not start attempt: ${err.message}`);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto py-12 px-4 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Loading clinical cases...</span>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900 tracking-tight">
          {t.cases.header}
        </h1>
        <p className="text-sm text-slate-600 mt-1 max-w-3xl leading-relaxed">
          {t.cases.description}
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cases.map((c) => {
          const isInitial = c.case_role === 'initial';
          return (
            <div
              key={c.id}
              className="bg-white rounded-2xl border border-slate-200 shadow-xs hover:shadow-md transition-all flex flex-col justify-between overflow-hidden group"
            >
              <div className="p-6 space-y-3">
                <div className="flex items-center justify-between gap-2">
                  <span
                    className={`inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider ${
                      isInitial
                        ? 'bg-blue-50 text-blue-700 border border-blue-200'
                        : 'bg-teal-50 text-teal-800 border border-teal-200'
                    }`}
                  >
                    {isInitial ? <BookOpen className="w-3 h-3" /> : <RefreshCw className="w-3 h-3" />}
                    <span>{isInitial ? t.cases.initialRole : t.cases.reassessmentRole}</span>
                  </span>

                  <span className="text-[10px] font-mono text-slate-400 font-bold">
                    v{c.version}
                  </span>
                </div>

                <h3 className="text-base font-bold text-slate-900 group-hover:text-medblue-600 transition-colors leading-snug">
                  {c.title}
                </h3>

                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                  <Tag className="w-3.5 h-3.5 text-slate-400" />
                  <span>{t.cases.objective}: <strong className="text-slate-700">{c.learning_objective}</strong></span>
                </div>

                <p className="text-xs text-slate-500 line-clamp-2 italic pt-1 border-t border-slate-100">
                  {c.disclaimer}
                </p>
              </div>

              <div className="p-6 pt-0">
                <button
                  onClick={() => handleStartCase(c.id)}
                  className="w-full py-2.5 px-4 rounded-xl text-sm font-bold text-medblue-700 bg-medblue-50 hover:bg-medblue-600 hover:text-white transition-all flex items-center justify-center gap-2 group/btn"
                >
                  <span>{t.cases.startCase}</span>
                  <ArrowRight className="w-4 h-4 transform group-hover/btn:translate-x-0.5 transition-transform" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
