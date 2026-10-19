import React from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  Compass,
  ArrowRight,
  Sparkles,
  ShieldCheck,
  HelpCircle,
} from 'lucide-react';
import { FeedbackRecord } from '../types';
import { SourceCard } from './SourceCard';
import { useLanguage } from '../i18n/LanguageContext';

interface FeedbackPanelProps {
  feedback: FeedbackRecord;
  onProceedLesson?: () => void;
  onProceedReassess?: () => void;
  recommendedLessonId?: string | null;
}

export const FeedbackPanel: React.FC<FeedbackPanelProps> = ({
  feedback,
  onProceedLesson,
  onProceedReassess,
  recommendedLessonId,
}) => {
  const { t } = useLanguage();
  const payload = feedback.payload;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden space-y-6 p-6">
      {/* Header with Source Badge */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-medblue-600" />
          <h3 className="text-base font-bold text-slate-900">
            {t.feedback.title}
          </h3>
        </div>

        <div>
          {feedback.source === 'llm' ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-purple-50 text-purple-700 border border-purple-200">
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              <span>{t.feedback.aiLabel} ({feedback.model || 'Claude'})</span>
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-teal-50 text-teal-800 border border-teal-200">
              <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
              <span>{t.feedback.fallbackLabel}</span>
            </span>
          )}
        </div>
      </div>

      {/* What You Got Right */}
      {payload.what_you_got_right && payload.what_you_got_right.length > 0 && (
        <div className="bg-emerald-50/50 border border-emerald-200 rounded-xl p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-800 flex items-center gap-1.5 mb-2.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>{t.feedback.whatRight}</span>
          </h4>
          <ul className="space-y-1.5 text-sm text-slate-700">
            {payload.what_you_got_right.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-600 font-bold">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* What Needs Work */}
      {payload.what_needs_work && payload.what_needs_work.length > 0 && (
        <div className="bg-amber-50/50 border border-amber-200 rounded-xl p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-amber-800 flex items-center gap-1.5 mb-2.5">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
            <span>{t.feedback.whatNeedsWork}</span>
          </h4>
          <ul className="space-y-1.5 text-sm text-slate-700">
            {payload.what_needs_work.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-amber-600 font-bold">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Why It Matters */}
      {payload.why_it_matters && (
        <div className="bg-medblue-50/40 border border-medblue-100 rounded-xl p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-medblue-800 flex items-center gap-1.5 mb-2">
            <Lightbulb className="w-4 h-4 text-medblue-600" />
            <span>{t.feedback.whyMatters}</span>
          </h4>
          <p className="text-sm text-slate-700 leading-relaxed font-normal">
            {payload.why_it_matters}
          </p>
        </div>
      )}

      {/* Citations & Verified Literature */}
      {payload.evidence_links && payload.evidence_links.length > 0 && (
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            <span>{t.feedback.citationsHeader} ({payload.evidence_links.length})</span>
          </h4>
          <div className="space-y-2">
            {payload.evidence_links.map((cite, idx) => (
              <SourceCard key={idx} citation={cite} />
            ))}
          </div>
        </div>
      )}

      {/* Reflection Prompt */}
      {payload.reflection_prompt && (
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1.5 mb-2">
            <Compass className="w-4 h-4 text-indigo-600" />
            <span>{t.feedback.reflectionPrompt}</span>
          </h4>
          <p className="text-sm text-slate-700 italic">
            "{payload.reflection_prompt}"
          </p>
        </div>
      )}

      {/* Uncertainty & Scope Note */}
      {payload.uncertainty_note && (
        <div className="text-xs text-slate-500 flex items-start gap-2 pt-2 border-t border-slate-100">
          <HelpCircle className="w-3.5 h-3.5 text-slate-400 mt-0.5 shrink-0" />
          <span>{payload.uncertainty_note}</span>
        </div>
      )}

      {/* Next Step Action Button */}
      <div className="pt-4 flex flex-col sm:flex-row gap-3">
        {onProceedLesson && (
          <button
            onClick={onProceedLesson}
            className="flex-1 py-3 px-5 rounded-xl font-bold text-white bg-medblue-600 hover:bg-medblue-700 shadow-md shadow-medblue-600/20 transition-all flex items-center justify-center gap-2 text-sm"
          >
            <span>{t.feedback.proceedLesson}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        )}

        {onProceedReassess && (
          <button
            onClick={onProceedReassess}
            className="py-3 px-5 rounded-xl font-bold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 transition-all flex items-center justify-center gap-2 text-sm"
          >
            <span>{t.feedback.skipToReassess}</span>
          </button>
        )}
      </div>
    </div>
  );
};
