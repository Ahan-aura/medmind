import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { useLanguage } from '../i18n/LanguageContext';

export const DisclaimerBanner: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 text-xs text-amber-900 flex items-center justify-center gap-2 text-center font-medium">
      <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
      <span>{t.disclaimer}</span>
    </div>
  );
};
