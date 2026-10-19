import React from 'react';
import { Award, CheckCircle2, XCircle } from 'lucide-react';
import { CriterionResult } from '../types';
import { useLanguage } from '../i18n/LanguageContext';

interface ScoreSummaryProps {
  score: number;
  maxScore: number;
  isCorrect?: boolean | null;
  criteria?: CriterionResult[] | null;
}

export const ScoreSummary: React.FC<ScoreSummaryProps> = ({
  score,
  maxScore,
  isCorrect,
  criteria = [],
}) => {
  const { t } = useLanguage();
  const percentage = Math.round((score / maxScore) * 100);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div className="bg-slate-900 text-white p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-bold text-sky-400 uppercase tracking-wider block mb-1">
            {t.feedback.scoreTitle}
          </span>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-black">{score.toFixed(1)}</span>
            <span className="text-xl text-slate-400 font-semibold">/ {maxScore.toFixed(1)} pts</span>
            <span className="ml-2 text-xs font-bold px-2 py-0.5 rounded-full bg-white/10 text-sky-300">
              {percentage}%
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {isCorrect ? (
            <div className="bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <span>Correct Primary Diagnosis</span>
            </div>
          ) : (
            <div className="bg-amber-500/20 border border-amber-500/30 text-amber-300 px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2">
              <XCircle className="w-5 h-5 text-amber-400" />
              <span>Suboptimal Diagnostic Path</span>
            </div>
          )}
        </div>
      </div>

      {criteria && criteria.length > 0 && (
        <div className="p-5">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
            Deterministic Rubric Criteria Evaluation
          </h4>
          <div className="space-y-2">
            {criteria.map((c) => (
              <div
                key={c.id}
                className={`p-3 rounded-lg border flex items-center justify-between text-sm ${
                  c.met
                    ? 'bg-emerald-50/50 border-emerald-200 text-slate-800'
                    : 'bg-slate-50 border-slate-200 text-slate-500'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  {c.met ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  ) : (
                    <XCircle className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                  <span className={`font-medium ${c.met ? 'text-slate-800' : 'text-slate-500'}`}>
                    {c.description}
                  </span>
                </div>
                <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                  c.met ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'
                }`}>
                  {c.met ? `+${c.points} pts` : '0 pts'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
