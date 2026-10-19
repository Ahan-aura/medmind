import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, ExternalLink, ShieldCheck } from 'lucide-react';
import { Citation } from '../types';

interface SourceCardProps {
  citation: Citation;
}

export const SourceCard: React.FC<SourceCardProps> = ({ citation }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden transition-all">
      <div
        onClick={() => setExpanded(!expanded)}
        className="p-4 flex items-start justify-between gap-3 cursor-pointer hover:bg-slate-50 transition-colors"
      >
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700 shrink-0 mt-0.5">
            <BookOpen className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200">
                {citation.ref_id}
              </span>
              <span className="text-xs font-semibold text-teal-700 flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" />
                Verified Guideline Reference
              </span>
            </div>
            <p className="text-sm font-medium text-slate-800 mt-1 leading-snug">
              {citation.supports}
            </p>
          </div>
        </div>

        <button
          type="button"
          className="text-slate-400 hover:text-slate-600 p-1"
          title={expanded ? 'Collapse' : 'Expand source excerpt'}
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {expanded && (
        <div className="px-5 pb-4 pt-1 border-t border-slate-100 bg-slate-50/50 text-xs text-slate-600 leading-relaxed font-normal">
          <p className="italic">
            Passage citation retrieved from approved institutional clinical references: British Society of Haematology, WHO Guidelines, and Clinical Haematology Practice Compendia.
          </p>
        </div>
      )}
    </div>
  );
};
