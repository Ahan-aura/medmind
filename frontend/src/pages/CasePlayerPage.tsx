import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PatientCard } from '../components/PatientCard';
import { LabTable } from '../components/LabTable';
import { BranchPanel } from '../components/BranchPanel';
import { DecisionForm } from '../components/DecisionForm';
import { Attempt } from '../types';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export const CasePlayerPage: React.FC = () => {
  const { id: attemptId } = useParams<{ id: string }>();
  const [attempt, setAttempt] = useState<Attempt | null>(null);
  const [selectedEvidence, setSelectedEvidence] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { t } = useLanguage();

  useEffect(() => {
    async function loadAttempt() {
      if (!attemptId) return;
      try {
        const data = await api.attempts.get(attemptId);
        setAttempt(data);
        if (data.selected_evidence && data.selected_evidence.length > 0) {
          setSelectedEvidence(data.selected_evidence);
        }
        if (data.state === 'SUBMITTED' || data.state === 'FEEDBACK_READY' || data.state === 'LESSON_DONE' || data.state === 'COMPLETED') {
          navigate(`/attempt/${attemptId}/feedback`);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load case attempt');
      } finally {
        setLoading(false);
      }
    }
    loadAttempt();
  }, [attemptId]);

  const handleToggleEvidence = (labId: string) => {
    setSelectedEvidence((prev) =>
      prev.includes(labId) ? prev.filter((id) => id !== labId) : [...prev, labId]
    );
  };

  const handleBranchStep = async (choiceId: string) => {
    if (!attempt || !attempt.current_node) return;
    try {
      const res = await api.attempts.step(attempt.id, attempt.current_node, choiceId);
      // Reload attempt data
      const updated = await api.attempts.get(attempt.id);
      setAttempt(updated);
    } catch (err: any) {
      alert(`Could not advance branch: ${err.message}`);
    }
  };

  const handleSubmitDecision = async (data: {
    selected_answer: string;
    reasoning_text: string;
    selected_evidence: string[];
    confidence: number;
  }) => {
    if (!attempt) return;
    setSubmitting(true);
    try {
      await api.attempts.submit(attempt.id, data);
      navigate(`/attempt/${attempt.id}/feedback`);
    } catch (err: any) {
      alert(`Submission error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center">
        <div className="w-8 h-8 border-3 border-medblue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-sm text-slate-500 font-medium">Preparing clinical simulation...</span>
      </div>
    );
  }

  if (error || !attempt) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm">
          {error || 'Attempt not found'}
        </div>
      </div>
    );
  }

  const caseView = attempt.case_view;

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 gap-2">
        <div>
          <span className="text-xs font-mono font-bold text-medblue-600 uppercase tracking-wider block">
            {caseView.id} · {caseView.learning_objective}
          </span>
          <h1 className="text-xl font-black text-slate-900 tracking-tight">
            {caseView.title}
          </h1>
        </div>

        <div className="text-xs text-slate-500 font-medium">
          State: <span className="font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">{attempt.state}</span>
        </div>
      </div>

      {/* Patient Presentation Card */}
      <PatientCard patient={caseView.patient} history={caseView.history} />

      {/* Laboratory Panel with Clickable Evidence Selection */}
      <LabTable
        labs={caseView.labs}
        selectedEvidence={selectedEvidence}
        onToggleEvidence={handleToggleEvidence}
        selectable={true}
      />

      {/* Branching Investigation Node (Smear, etc.) */}
      {attempt.current_node_data && (
        <BranchPanel
          currentNode={attempt.current_node_data}
          onSelectChoice={handleBranchStep}
        />
      )}

      {/* Decision Form with Diagnostic Choices, Evidence, Reasoning & Confidence */}
      <DecisionForm
        question={caseView.question}
        options={caseView.options}
        labs={caseView.labs}
        selectedEvidence={selectedEvidence}
        onToggleEvidence={handleToggleEvidence}
        onSubmit={handleSubmitDecision}
        loading={submitting}
      />
    </div>
  );
};
