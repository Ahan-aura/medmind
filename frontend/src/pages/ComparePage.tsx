import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Award, ArrowRight, CheckCircle2, TrendingUp, RefreshCw, BarChart2 } from 'lucide-react';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export const ComparePage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [progressData, setProgressData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { t } = useLanguage();

  useEffect(() => {
    async function load() {
      try {
        const data = await api.progress.getMe();
        setProgressData(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Loading learning transfer comparison...</span>
      </div>
    );
  }

  const primaryObj = progressData?.objectives?.[0] || {
    learning_objective: 'LO-MICROCYTIC-01',
    initial_score: 5.0,
    initial_max: 10.0,
    reassessment_score: 9.0,
    reassessment_max: 10.0,
    delta: 4.0,
    criteria_newly_met: [
      'Identified normal ferritin as ruling out simple iron deficiency',
      'Recognised normal RDW characteristic of uniform microcytic cells in thalassaemia trait'
    ]
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div>
        <span className="text-xs font-mono font-bold text-teal-600 uppercase tracking-wider block">
          Knowledge Transfer & Mastery Verification
        </span>
        <h1 className="text-2xl font-black text-slate-900 tracking-tight">
          {t.compare.title}
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          {t.compare.subtitle}
        </p>
      </div>

      {/* Side-by-Side Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Initial Attempt Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              {t.compare.initialScore}
            </span>
            <span className="text-xs font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-600">
              CASE-FATIGUE-01
            </span>
          </div>

          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-black text-slate-800">
              {primaryObj.initial_score ?? 5.0}
            </span>
            <span className="text-lg text-slate-400 font-semibold">
              / {primaryObj.initial_max ?? 10.0} pts
            </span>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Initial encounter with Alex (Fatigue with microcytosis). Encountered difficulty differentiating red cell indices.
          </p>
        </div>

        {/* Reassessment Attempt Card */}
        <div className="bg-gradient-to-br from-teal-50 to-emerald-50 rounded-2xl border border-teal-200 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-teal-200/60">
            <span className="text-xs font-bold text-teal-900 uppercase tracking-wider flex items-center gap-1.5">
              <RefreshCw className="w-3.5 h-3.5 text-teal-600" />
              <span>{t.compare.reassessScore}</span>
            </span>
            <span className="text-xs font-mono bg-white px-2 py-0.5 rounded text-teal-800 font-bold border border-teal-200">
              CASE-FATIGUE-02
            </span>
          </div>

          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-black text-teal-900">
              {primaryObj.reassessment_score ?? 9.0}
            </span>
            <span className="text-lg text-teal-600 font-semibold">
              / {primaryObj.reassessment_max ?? 10.0} pts
            </span>
            <span className="ml-3 text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-600 text-white flex items-center gap-1">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>+{primaryObj.delta ?? 4.0} Gain</span>
            </span>
          </div>
          <p className="text-xs text-teal-800 leading-relaxed">
            Transfer case with Jordan (Microcytosis with normal ferritin). Successfully distinguished beta-thalassaemia trait using ferritin and RDW!
          </p>
        </div>
      </div>

      {/* Newly Met Criteria */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <Award className="w-4 h-4 text-amber-500" />
          <span>{t.compare.newlyMet}</span>
        </h3>

        <div className="space-y-2">
          {(primaryObj.criteria_newly_met && primaryObj.criteria_newly_met.length > 0
            ? primaryObj.criteria_newly_met
            : [
                'Identified normal ferritin as ruling out simple iron deficiency',
                'Recognised normal RDW characteristic of uniform microcytic cells in thalassaemia trait',
                'Synthesized family history and high RBC count into final differential'
              ]
          ).map((crit: string, idx: number) => (
            <div key={idx} className="p-3 rounded-lg bg-emerald-50/70 border border-emerald-200 flex items-center gap-3 text-sm text-emerald-950 font-medium">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>{crit}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-2">
        <button
          onClick={() => navigate('/progress')}
          className="w-full py-3.5 px-6 rounded-xl font-bold text-white bg-medblue-600 hover:bg-medblue-700 shadow-md shadow-medblue-600/20 transition-all flex items-center justify-center gap-2 text-sm"
        >
          <BarChart2 className="w-4 h-4" />
          <span>{t.compare.viewProgress}</span>
        </button>
      </div>
    </div>
  );
};
