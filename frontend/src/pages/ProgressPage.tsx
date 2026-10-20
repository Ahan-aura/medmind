import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { BarChart2, Gauge, AlertCircle, Award, CheckCircle, ArrowRight } from 'lucide-react';
import { LearnerProgress } from '../types';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export const ProgressPage: React.FC = () => {
  const [progress, setProgress] = useState<LearnerProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { t } = useLanguage();

  useEffect(() => {
    async function load() {
      try {
        const data = await api.progress.getMe();
        setProgress(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load learner progress');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Computing longitudinal progress metrics...</span>
      </div>
    );
  }

  if (error || !progress) {
    return (
      <div className="max-w-5xl mx-auto py-12 px-4">
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error || 'No progress records available'}
        </div>
      </div>
    );
  }

  const chartData = (progress.objectives || []).map((o) => ({
    objective: o.learning_objective,
    Initial: o.initial_score ?? 0,
    Reassessment: o.reassessment_score ?? 0,
  }));

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      <div>
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">
            {t.progress.title}
          </h1>
          {((progress as any).is_sample_data || (import.meta as any).env?.VITE_DEMO_MODE === 'true') && (
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-300 uppercase">
              Sample Data
            </span>
          )}
        </div>
        <p className="text-sm text-slate-500 mt-1">
          Tracking clinical reasoning gains, confidence calibration, and concept transfer for {progress.display_name}.
        </p>
      </div>

      {/* 1. Objective Mastery Comparison (Initial vs Reassessment) */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart2 className="w-5 h-5 text-medblue-600" />
            <h3 className="text-base font-bold text-slate-900">
              {t.progress.objectivesHeader}
            </h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">Real Calculated Scores</span>
        </div>

        {chartData.length > 0 ? (
          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="objective" tick={{ fontSize: 12, fill: '#64748b' }} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 12, fill: '#64748b' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Bar dataKey="Initial" fill="#94a3b8" radius={[4, 4, 0, 0]} name="Initial Encounter Score" />
                <Bar dataKey="Reassessment" fill="#0e87eb" radius={[4, 4, 0, 0]} name="Reassessment Transfer Score" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="text-xs text-slate-500 py-6 text-center">Complete both initial and reassessment cases to generate comparative transfer analytics.</p>
        )}
      </div>

      {/* 2. Confidence Calibration Panel */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Gauge className="w-5 h-5 text-indigo-600" />
            <h3 className="text-base font-bold text-slate-900">
              {t.progress.calibrationHeader}
            </h3>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
              {progress.calibration_summary.calibrated} Calibrated
            </span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-50 text-amber-700 border border-amber-200">
              {progress.calibration_summary.overconfident} Overconfident
            </span>
          </div>
        </div>

        <p className="text-xs text-slate-500 leading-relaxed font-normal">
          {t.progress.calibrationDesc}
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
              <tr>
                <th className="py-2.5 px-3">Reported Confidence</th>
                <th className="py-2.5 px-3">Diagnostic Accuracy</th>
                <th className="py-2.5 px-3">Total Attempts</th>
                <th className="py-2.5 px-3">Calibration Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {progress.calibration.map((pt) => {
                const isUnder = pt.confidence_bin <= 40 && pt.accuracy > 60;
                const isOver = pt.confidence_bin >= 80 && pt.accuracy < 60;
                return (
                  <tr key={pt.confidence_bin} className="hover:bg-slate-50/50">
                    <td className="py-2.5 px-3 font-bold font-mono text-slate-800">
                      {pt.confidence_bin}%
                    </td>
                    <td className="py-2.5 px-3 font-mono font-bold text-slate-900">
                      {pt.count > 0 ? `${pt.accuracy.toFixed(1)}%` : '—'}
                    </td>
                    <td className="py-2.5 px-3 text-slate-600">
                      {pt.count} attempt{pt.count !== 1 ? 's' : ''}
                    </td>
                    <td className="py-2.5 px-3">
                      {pt.count === 0 ? (
                        <span className="text-slate-400">No data</span>
                      ) : isOver ? (
                        <span className="text-amber-700 font-bold bg-amber-50 px-2 py-0.5 rounded">
                          Overconfident Gap
                        </span>
                      ) : isUnder ? (
                        <span className="text-blue-700 font-bold bg-blue-50 px-2 py-0.5 rounded">
                          Underconfident
                        </span>
                      ) : (
                        <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded">
                          Calibrated
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* 3. Observed Misconceptions History */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-amber-600" />
          <span>{t.progress.misconceptionHistory}</span>
        </h3>

        {progress.misconceptions && progress.misconceptions.length > 0 ? (
          <div className="space-y-2.5">
            {progress.misconceptions.map((m) => (
              <div
                key={m.id}
                className="p-3.5 rounded-xl border border-slate-200 flex items-center justify-between text-xs hover:bg-slate-50 transition-colors"
              >
                <div>
                  <span className="font-bold text-slate-800 block text-sm mb-0.5">
                    {m.name}
                  </span>
                  <span className="text-slate-400 font-mono text-[11px]">{m.id}</span>
                </div>
                <div className="text-right">
                  <span className="font-bold text-medblue-700 bg-medblue-50 px-2.5 py-1 rounded-full border border-medblue-200">
                    {m.times_seen} {t.progress.timesObserved}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 py-3">No reasoning misconceptions recorded. Excellent clinical accuracy!</p>
        )}
      </div>
    </div>
  );
};
