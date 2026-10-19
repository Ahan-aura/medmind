import React from 'react';
import { GitBranch, Eye, ArrowRight, CheckCircle2 } from 'lucide-react';
import { BranchNode } from '../types';
import { useLanguage } from '../i18n/LanguageContext';

interface BranchPanelProps {
  currentNode: BranchNode | null | undefined;
  onSelectChoice: (choiceId: string) => void;
  loading?: boolean;
}

export const BranchPanel: React.FC<BranchPanelProps> = ({
  currentNode,
  onSelectChoice,
  loading = false,
}) => {
  const { t } = useLanguage();

  if (!currentNode || !currentNode.choices || currentNode.choices.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div className="bg-slate-50 border-b border-slate-200 px-5 py-3.5 flex items-center gap-2">
        <GitBranch className="w-5 h-5 text-indigo-600" />
        <h3 className="text-sm font-bold text-slate-900 tracking-wide">
          {t.player.branchingHeader}
        </h3>
      </div>

      <div className="p-5 space-y-4">
        {/* Node prompt or reveal text */}
        {(currentNode.text || currentNode.reveal) && (
          <div className="bg-indigo-50/50 border border-indigo-100 rounded-lg p-4 flex items-start gap-3">
            <Eye className="w-5 h-5 text-indigo-600 mt-0.5 shrink-0" />
            <div className="text-sm text-slate-800 leading-relaxed font-normal">
              {currentNode.reveal ? (
                <div>
                  <span className="font-bold text-indigo-900 block mb-1">
                    {t.player.revealedSmear}:
                  </span>
                  {currentNode.reveal}
                </div>
              ) : (
                currentNode.text
              )}
            </div>
          </div>
        )}

        {/* Choice buttons */}
        <div className="flex flex-wrap gap-3 pt-1">
          {currentNode.choices.map((choice) => (
            <button
              key={choice.id}
              onClick={() => onSelectChoice(choice.id)}
              disabled={loading}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-semibold bg-indigo-600 hover:bg-indigo-700 text-white shadow-xs transition-colors disabled:opacity-50"
            >
              <span>{choice.label}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
