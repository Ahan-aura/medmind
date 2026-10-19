import React from 'react';
import { User, Calendar, FileText, HeartPulse } from 'lucide-react';
import { PatientInfo } from '../types';
import { useLanguage } from '../i18n/LanguageContext';

interface PatientCardProps {
  patient: PatientInfo;
  history: string;
}

export const PatientCard: React.FC<PatientCardProps> = ({ patient, history }) => {
  const { t } = useLanguage();

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div className="bg-gradient-to-r from-medblue-900 to-slate-900 text-white px-5 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
            <HeartPulse className="w-4 h-4 text-sky-300" />
          </div>
          <div>
            <h3 className="text-sm font-bold tracking-wide uppercase text-sky-200">
              {t.player.patientHistory}
            </h3>
            <span className="text-xs text-slate-300">Fictional Educational Profile</span>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs bg-white/10 px-3 py-1.5 rounded-lg border border-white/10">
          <span className="font-semibold">{patient.name}</span>
          <span className="text-white/40">|</span>
          <span>{patient.age} y/o</span>
          <span className="text-white/40">|</span>
          <span className="capitalize">{patient.sex}</span>
        </div>
      </div>

      <div className="p-5">
        <div className="flex items-start gap-3">
          <FileText className="w-5 h-5 text-medblue-600 mt-0.5 shrink-0" />
          <p className="text-sm text-slate-700 leading-relaxed font-normal">
            {history}
          </p>
        </div>
      </div>
    </div>
  );
};
