import React, { useState } from 'react';
import { Stethoscope, CheckCircle2, AlertCircle, Sparkles } from 'lucide-react';
import { OptionItem, LabItem } from '../types';
import { ConfidencePicker } from './ConfidencePicker';
import { useLanguage } from '../i18n/LanguageContext';

interface DecisionFormProps {
  question: string;
  options: OptionItem[];
  labs: LabItem[];
  selectedEvidence: string[];
  onToggleEvidence: (id: string) => void;
  onSubmit: (data: {
    selected_answer: string;
    reasoning_text: string;
    selected_evidence: string[];
    confidence: number;
  }) => Promise<void>;
  loading?: boolean;
}

export const DecisionForm: React.FC<DecisionFormProps> = ({
  question,
  options,
  labs,
  selectedEvidence,
  onToggleEvidence,
  onSubmit,
  loading = false,
}) => {
  const { t } = useLanguage();
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [reasoningText, setReasoningText] = useState<string>('');
  const [confidence, setConfidence] = useState<number>(80);
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    if (!selectedAnswer) {
      setValidationError('Please select a diagnostic interpretation before submitting.');
      return;
    }
    if (selectedEvidence.length === 0) {
      setValidationError('Please select at least one supporting laboratory or clinical finding from the table.');
      return;
    }
    if (!reasoningText.trim()) {
      setValidationError('Please write a brief justification of your clinical reasoning.');
      return;
    }

    await onSubmit({
      selected_answer: selectedAnswer,
      reasoning_text: reasoningText,
      selected_evidence: selectedEvidence,
      confidence,
    });
  };

  const handleFillDemoData = () => {
    // Demo auto-fill helper
    setSelectedAnswer('A');
    setReasoningText('Patient presents with microcytic indices (MCV 68 fL) and depleted iron stores (ferritin 8 ng/mL) resulting from menorrhagia and dietary deficiency.');
    // toggle key evidence if not already present
    ['mcv', 'ferritin', 'rdw'].forEach((id) => {
      if (!selectedEvidence.includes(id)) {
        onToggleEvidence(id);
      }
    });
    setConfidence(80);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div className="bg-slate-50 border-b border-slate-200 px-5 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Stethoscope className="w-5 h-5 text-medblue-600" />
          <h3 className="text-sm font-bold text-slate-900 tracking-wide">
            {t.player.decisionHeader}
          </h3>
        </div>
        <button
          type="button"
          onClick={handleFillDemoData}
          className="text-xs text-amber-600 hover:text-amber-800 font-semibold bg-amber-50 hover:bg-amber-100 px-2.5 py-1 rounded-md border border-amber-200 flex items-center gap-1 transition-colors"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Demo Preset</span>
        </button>
      </div>

      <div className="p-6 space-y-6">
        {validationError && (
          <div className="bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded-lg text-sm flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{validationError}</span>
          </div>
        )}

        {/* Diagnostic Question and Options */}
        <div>
          <label className="text-sm font-bold text-slate-900 block mb-3 leading-snug">
            {question}
          </label>
          <div className="space-y-2.5">
            {options.map((opt) => {
              const isSelected = selectedAnswer === opt.id;
              return (
                <label
                  key={opt.id}
                  className={`flex items-start gap-3 p-3.5 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-medblue-50/70 border-medblue-500 ring-2 ring-medblue-500/20'
                      : 'bg-white hover:bg-slate-50 border-slate-200'
                  }`}
                >
                  <input
                    type="radio"
                    name="interpretation"
                    value={opt.id}
                    checked={isSelected}
                    onChange={(e) => setSelectedAnswer(e.target.value)}
                    className="w-4 h-4 text-medblue-600 mt-0.5 border-slate-300 focus:ring-medblue-500"
                  />
                  <span className="text-sm font-medium text-slate-800 leading-snug">
                    <span className="font-bold mr-1.5 text-medblue-700">{opt.id}.</span>
                    {opt.text}
                  </span>
                </label>
              );
            })}
          </div>
        </div>

        {/* Selected Evidence Badges */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-bold text-slate-800">
              {t.player.evidenceSelection} ({selectedEvidence.length} selected)
            </label>
            <span className="text-xs text-slate-500">
              Select findings from the Laboratory Panel above
            </span>
          </div>
          {selectedEvidence.length === 0 ? (
            <div className="p-3 rounded-lg border border-dashed border-slate-200 text-xs text-slate-500 text-center bg-slate-50">
              No evidence selected yet. Click any row in the lab table above to add evidence.
            </div>
          ) : (
            <div className="flex flex-wrap gap-2">
              {selectedEvidence.map((evId) => {
                const lab = labs.find((l) => l.id === evId);
                return (
                  <span
                    key={evId}
                    className="inline-flex items-center gap-1.5 bg-medblue-50 text-medblue-800 text-xs font-semibold px-2.5 py-1 rounded-md border border-medblue-200"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-medblue-600" />
                    <span>{lab ? `${lab.test}: ${lab.value} ${lab.unit}` : evId}</span>
                    <button
                      type="button"
                      onClick={() => onToggleEvidence(evId)}
                      className="ml-1 text-medblue-600 hover:text-medblue-900 font-bold"
                    >
                      ×
                    </button>
                  </span>
                );
              })}
            </div>
          )}
        </div>

        {/* Clinical Reasoning Justification */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-bold text-slate-800">
              {t.player.reasoningLabel}
            </label>
            <span className="text-xs text-slate-500">
              {reasoningText.length} / 2000 characters
            </span>
          </div>
          <textarea
            rows={4}
            maxLength={2000}
            value={reasoningText}
            onChange={(e) => setReasoningText(e.target.value)}
            placeholder={t.player.reasoningPlaceholder}
            className="w-full rounded-xl border border-slate-300 p-3 text-sm focus:border-medblue-500 focus:ring-2 focus:ring-medblue-200 outline-none transition-all resize-y"
          />
        </div>

        {/* Confidence Picker */}
        <ConfidencePicker
          value={confidence}
          onChange={setConfidence}
          disabled={loading}
        />

        {/* Submit Button */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-6 rounded-xl text-base font-bold text-white bg-medblue-600 hover:bg-medblue-700 shadow-md shadow-medblue-600/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>{t.player.submitting}</span>
              </>
            ) : (
              <span>{t.player.submitBtn}</span>
            )}
          </button>
        </div>
      </div>
    </form>
  );
};
