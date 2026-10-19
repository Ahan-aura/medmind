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
import { GraduationCap, Users, AlertTriangle, TrendingUp, Gauge, ShieldCheck } from 'lucide-react';
import { TeacherSummary } from '../types';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export const TeacherPage: React.FC = () => {
  const [summary, setSummary] = useState<TeacherSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { t } = useLanguage();

  useEffect(() => {
    async function load() {
      try {
        const data = await api.teacher.getSummary('cohort-med-2026-alpha');
        setSummary(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load faculty cohort analytics');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-purple-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Aggregating cohort-wide learning analytics...</span>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="max-w-6xl mx-auto py-12 px-4">
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error || 'Cohort analytics unavailable'}
        </div>
      </div>
    );
  }

  const chartData = (summary.objective_averages || []).map((oa) => ({
    objective: oa.learning_objective,
    Initial: oa.avg_initial_score,
    Reassessment: oa.avg_reassessment_score,
  }));

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-bold text-purple-700 bg-purple-50 px-2.5 py-0.5 rounded-full border border-purple-200 uppercase tracking-wider">
              Faculty / Educator View
            </span>
            <span className="text-xs text-slate-400 font-semibold">Privacy-Preserving Cohort Aggregates</span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            {t.teacher.title}
          </h1>
          <p className="text-sm text-slate-500">
            {summary.cohort_name}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="bg-white border border-slate-200 rounded-xl px-4 py-2 text-right shadow-xs">
            <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
              {t.teacher.studentCount}
            </span>
            <span className="text-xl font-black text-slate-800 flex items-center justify-end gap-1.5">
              <Users className="w-4 h-4 text-purple-600" />
              <span>{summary.student_count}</span>
            </span>
          </div>
        </div>
      </div>

      {/* Panel 1: Cohort Average Score Comparison: Initial vs Reassessment */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-purple-600" />
            <h3 className="text-base font-bold text-slate-900">
              {t.teacher.cohortAverages}
            </h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">Percentage Normalized</span>
        </div>

        <div className="h-64 w-full pt-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="objective" tick={{ fontSize: 12, fill: '#64748b' }} />
              <YAxis unit="%" domain={[0, 100]} tick={{ fontSize: 12, fill: '#64748b' }} />
              <Tooltip
                formatter={(val: any) => [`${val}%`, '']}
                contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Bar dataKey="Initial" fill="#cbd5e1" radius={[4, 4, 0, 0]} name="Avg Initial Case Score" />
              <Bar dataKey="Reassessment" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Avg Reassessment Transfer Score" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Grid of Panel 2 (Misconceptions) & Panel 3 (Calibration) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Panel 2: Top 5 Recurring Misconceptions in Class */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              <h3 className="text-base font-bold text-slate-900">
                {t.teacher.commonMisconceptions}
              </h3>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed font-normal">
              {t.teacher.misconceptionTableDesc}
            </p>

            <div className="mt-4 space-y-2.5">
              {summary.top_misconceptions.map((mc, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-amber-50/60 border border-amber-200/70 flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <span className="w-5 h-5 rounded-full bg-amber-200 text-amber-900 font-bold flex items-center justify-center text-[10px] shrink-0">
                      {idx + 1}
                    </span>
                    <span className="font-semibold text-slate-800">
                      {mc.name}
                    </span>
                  </div>
                  <span className="font-bold text-amber-900 bg-amber-100 px-2 py-0.5 rounded text-[11px] shrink-0">
                    {mc.students} learner{mc.students !== 1 ? 's' : ''}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-2 text-[11px] text-slate-400 italic border-t border-slate-100">
            Rule: Only displayed for cohorts with ≥ 3 learners to preserve student anonymity.
          </div>
        </div>

        {/* Panel 3: Class Confidence Calibration Matrix */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <div className="flex items-center gap-2">
            <Gauge className="w-5 h-5 text-purple-600" />
            <h3 className="text-base font-bold text-slate-900">
              {t.teacher.classCalibration}
            </h3>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed font-normal">
            Aggregated distribution of student confidence vs correctness across all case encounters.
          </p>

          <div className="overflow-x-auto pt-2">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-3">Reported Confidence</th>
                  <th className="py-2.5 px-3">Accuracy</th>
                  <th className="py-2.5 px-3">Cohort Attempts</th>
                  <th className="py-2.5 px-3">Pedagogical Insight</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {summary.calibration_matrix.map((row) => {
                  const isOver = row.confidence_bin >= 80 && row.accuracy < 65;
                  return (
                    <tr key={row.confidence_bin} className="hover:bg-slate-50/50">
                      <td className="py-2.5 px-3 font-mono font-bold text-slate-800">
                        {row.confidence_bin}%
                      </td>
                      <td className="py-2.5 px-3 font-mono font-bold text-slate-900">
                        {row.accuracy.toFixed(1)}%
                      </td>
                      <td className="py-2.5 px-3 text-slate-600">
                        {row.total_attempts} attempts
                      </td>
                      <td className="py-2.5 px-3">
                        {isOver ? (
                          <span className="text-amber-700 font-bold bg-amber-50 px-2 py-0.5 rounded text-[10px]">
                            High Overconfidence
                          </span>
                        ) : (
                          <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded text-[10px]">
                            Balanced
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
      </div>
    </div>
  );
};
