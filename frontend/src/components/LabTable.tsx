import React from 'react';
import { ArrowDown, ArrowUp, Check, FlaskConical } from 'lucide-react';
import { LabItem } from '../types';
import { useLanguage } from '../i18n/LanguageContext';

interface LabTableProps {
  labs: LabItem[];
  selectedEvidence?: string[];
  onToggleEvidence?: (labId: string) => void;
  selectable?: boolean;
}

export const LabTable: React.FC<LabTableProps> = ({
  labs,
  selectedEvidence = [],
  onToggleEvidence,
  selectable = false,
}) => {
  const { t } = useLanguage();

  const getFlagBadge = (flag: 'low' | 'high' | 'normal') => {
    switch (flag) {
      case 'low':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300">
            <ArrowDown className="w-3.5 h-3.5 stroke-[2.5]" />
            <span>LOW</span>
          </span>
        );
      case 'high':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300">
            <ArrowUp className="w-3.5 h-3.5 stroke-[2.5]" />
            <span>HIGH</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
            <Check className="w-3 h-3" />
            <span>Normal</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div className="bg-slate-50 border-b border-slate-200 px-5 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FlaskConical className="w-5 h-5 text-medblue-600" />
          <h3 className="text-sm font-bold text-slate-900 tracking-wide">
            {t.player.labsHeader}
          </h3>
        </div>
        {selectable && (
          <span className="text-xs text-medblue-600 font-semibold bg-medblue-50 px-2.5 py-1 rounded-full border border-medblue-200">
            Click row to select as evidence
          </span>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-100/75 text-xs uppercase font-semibold text-slate-500 border-b border-slate-200">
            <tr>
              {selectable && <th className="py-3 px-4 w-12 text-center">Cite</th>}
              <th className="py-3 px-4">Test Name</th>
              <th className="py-3 px-4">Result Value</th>
              <th className="py-3 px-4">Reference Interval</th>
              <th className="py-3 px-4">Clinical Flag</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {labs.map((lab) => {
              const isSelected = selectedEvidence.includes(lab.id);
              return (
                <tr
                  key={lab.id}
                  onClick={() => selectable && onToggleEvidence && onToggleEvidence(lab.id)}
                  className={`transition-colors ${
                    selectable ? 'cursor-pointer hover:bg-medblue-50/50' : ''
                  } ${isSelected ? 'bg-medblue-50/80 font-medium' : ''}`}
                >
                  {selectable && (
                    <td className="py-3 px-4 text-center">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => {}} // handled by row onClick
                        className="w-4 h-4 text-medblue-600 rounded border-slate-300 focus:ring-medblue-500 pointer-events-none"
                      />
                    </td>
                  )}
                  <td className="py-3 px-4 font-semibold text-slate-800">
                    {lab.test}
                  </td>
                  <td className="py-3 px-4 text-slate-900 font-mono font-bold">
                    {lab.value}{' '}
                    <span className="text-xs font-normal text-slate-500">
                      {lab.unit}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-500 font-mono text-xs">
                    {lab.ref} {lab.unit}
                  </td>
                  <td className="py-3 px-4">
                    {getFlagBadge(lab.flag)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
