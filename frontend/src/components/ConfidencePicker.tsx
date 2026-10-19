import React from 'react';
import { Gauge } from 'lucide-react';
import { useLanguage } from '../i18n/LanguageContext';

interface ConfidencePickerProps {
  value: number;
  onChange: (val: number) => void;
  disabled?: boolean;
}

const CONFIDENCE_LEVELS = [
  { value: 20, label: '20%', desc: 'Uncertain / Guess' },
  { value: 40, label: '40%', desc: 'Low Confidence' },
  { value: 60, label: '60%', desc: 'Moderate' },
  { value: 80, label: '80%', desc: 'Strong Confidence' },
  { value: 100, label: '100%', desc: 'Absolute Certainty' },
];

export const ConfidencePicker: React.FC<ConfidencePickerProps> = ({
  value,
  onChange,
  disabled = false,
}) => {
  const { t } = useLanguage();

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="text-sm font-bold text-slate-800 flex items-center gap-1.5">
          <Gauge className="w-4 h-4 text-medblue-600" />
          <span>{t.player.confidenceLabel}</span>
        </label>
        <span className="text-xs text-slate-500 font-medium">
          {t.player.confidenceHint}
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
        {CONFIDENCE_LEVELS.map((lvl) => {
          const isSelected = value === lvl.value;
          return (
            <button
              type="button"
              key={lvl.value}
              disabled={disabled}
              onClick={() => onChange(lvl.value)}
              className={`p-3 rounded-xl border text-center transition-all ${
                isSelected
                  ? 'bg-medblue-600 text-white border-medblue-600 shadow-md shadow-medblue-600/20 scale-[1.02]'
                  : 'bg-white hover:bg-slate-50 text-slate-700 border-slate-200 hover:border-slate-300'
              } disabled:opacity-50`}
            >
              <div className="text-base font-black leading-tight">
                {lvl.label}
              </div>
              <div className={`text-[10px] mt-0.5 font-medium leading-tight ${
                isSelected ? 'text-blue-100' : 'text-slate-500'
              }`}>
                {lvl.desc}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
