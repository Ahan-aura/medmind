import React from 'react';
import { AlertTriangle, AlertCircle } from 'lucide-react';
import { useLanguage } from '../i18n/LanguageContext';
import { IS_DEMO_MODE } from '../api/client';

export const DisclaimerBanner: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div className="flex flex-col">
      {IS_DEMO_MODE && (
        <div className="bg-amber-500 text-slate-950 px-4 py-2 text-xs font-black tracking-wide flex items-center justify-center gap-2 text-center uppercase shadow-sm">
          <AlertCircle className="w-4 h-4 text-slate-950 shrink-0 stroke-[3]" />
          <span>SIMULATION MODE: no server, sample data, scores are not real.</span>
        </div>
      )}
      <div className="bg-slate-900 border-b border-slate-800 px-4 py-2 text-xs text-amber-200 flex items-center justify-center gap-2 text-center font-medium">
        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
        <span>{t.disclaimer}</span>
      </div>
    </div>
  );
};
