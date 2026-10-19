import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { PlayCircle, ChevronRight, X, Sparkles, Clock, CheckCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface DemoStep {
  time: string;
  title: string;
  desc: string;
  path: string;
  hint: string;
}

const DEMO_STEPS: DemoStep[] = [
  {
    time: "0:00 - 0:30",
    title: "1. Problem & Persona",
    desc: "Medical learners need safe practice connecting lab values to pathophysiological reasoning.",
    path: "/login",
    hint: "Click Quick Demo: Student to sign in instantly as Alex Mercer."
  },
  {
    time: "0:30 - 1:15",
    title: "2. Patient & Lab Panel",
    desc: "Inspect the fictional young adult case with progressive fatigue and red cell indices.",
    path: "/cases",
    hint: "Open 'Persistent Fatigue in a Young Adult' to see CBC, smear options, and flags."
  },
  {
    time: "1:15 - 2:00",
    title: "3. Reasoning & Confidence",
    desc: "Select evidence, formulate an explanation, and rate diagnostic confidence (20-100%).",
    path: "/cases",
    hint: "In the case player, choose Iron Deficiency Anaemia, check low MCV and ferritin, and rate confidence 80%."
  },
  {
    time: "2:00 - 2:45",
    title: "4. Grounded AI Tutor & Citations",
    desc: "Review deterministic rubric scoring and AI explanation citing verified guidelines.",
    path: "/progress",
    hint: "Notice how every claim is linked to an approved reference card (REF-IDA-001) with zero hallucination."
  },
  {
    time: "2:45 - 3:30",
    title: "5. Targeted Lesson & Reassessment",
    desc: "Identified misconception triggers a bite-sized module, then tests transfer on Jordan's case.",
    path: "/cases",
    hint: "The system tests if the student can now distinguish microcytosis with normal ferritin (Thalassaemia minor)."
  },
  {
    time: "3:30 - 4:00",
    title: "6. Progress & Faculty Analytics",
    desc: "View student score gain (+3.0 delta) and class-wide misconception clustering.",
    path: "/teacher",
    hint: "Switch to Faculty Dashboard to see cohort-level learning gaps and calibration."
  }
];

export const DemoWalkthroughBar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const navigate = useNavigate();
  const { user, quickLogin } = useAuth();

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 z-50 bg-medblue-600 hover:bg-medblue-700 text-white px-4 py-2 rounded-full shadow-lg flex items-center gap-2 text-sm font-semibold transition-all transform hover:scale-105"
      >
        <PlayCircle className="w-5 h-5 text-amber-300" />
        <span>Open 4-Min Demo Script</span>
      </button>
    );
  }

  const step = DEMO_STEPS[currentStep];

  const handleNext = async () => {
    const nextIdx = (currentStep + 1) % DEMO_STEPS.length;
    setCurrentStep(nextIdx);
    
    // Auto-assist during demo navigation
    if (nextIdx === 0 && !user) {
      navigate('/login');
    } else if (nextIdx === 1) {
      if (!user) await quickLogin('student');
      navigate('/cases');
    } else if (nextIdx === 5) {
      if (user?.role !== 'teacher') {
        await quickLogin('teacher');
      }
      navigate('/teacher');
    } else {
      navigate(DEMO_STEPS[nextIdx].path);
    }
  };

  return (
    <div className="bg-slate-900 border-b border-slate-800 text-white px-4 py-2.5 shadow-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3 text-sm">
        <div className="flex items-center gap-3">
          <div className="bg-amber-400/20 text-amber-300 px-2 py-0.5 rounded text-xs font-mono font-bold flex items-center gap-1 border border-amber-400/30">
            <Clock className="w-3.5 h-3.5" />
            <span>{step.time}</span>
          </div>
          <div>
            <span className="font-bold text-amber-400 mr-2">{step.title}</span>
            <span className="text-slate-300 text-xs hidden sm:inline">{step.desc}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="text-xs text-amber-200/80 bg-slate-800/80 px-2.5 py-1 rounded border border-slate-700 hidden lg:block">
            <span className="font-semibold text-white">Hint:</span> {step.hint}
          </div>

          <button
            onClick={handleNext}
            className="bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold px-3 py-1 rounded text-xs flex items-center gap-1 transition-colors"
          >
            <span>Next ({currentStep + 1}/6)</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => setIsOpen(false)}
            className="text-slate-400 hover:text-slate-200 p-1"
            title="Minimize"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
