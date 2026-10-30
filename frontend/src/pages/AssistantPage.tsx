import React, { useState, useEffect, useRef } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  Sparkles,
  Send,
  BookOpen,
  GraduationCap,
  AlertCircle,
  HelpCircle,
  ChevronRight,
  Shield,
  RotateCcw,
  Bot,
  User as UserIcon,
  CheckCircle2,
  ExternalLink,
  X,
  Stethoscope,
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import {
  ChatMessageUI,
  StarterPromptGroup,
  AssistantCitation,
  RecommendedLessonItem,
} from '../types';

export const AssistantPage: React.FC = () => {
  const { user } = useAuth();
  const { t, language } = useLanguage();
  const [searchParams] = useSearchParams();

  const caseContextId = searchParams.get('caseId');
  const lessonContextId = searchParams.get('lessonId');

  const [promptGroups, setPromptGroups] = useState<StarterPromptGroup[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [messages, setMessages] = useState<ChatMessageUI[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedCitation, setSelectedCitation] = useState<AssistantCitation | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Load starter prompts
  useEffect(() => {
    async function loadPrompts() {
      try {
        const res = await api.assistant.getPrompts();
        if (res.groups) {
          setPromptGroups(res.groups);
        }
      } catch (err) {
        console.warn('Could not load assistant prompts:', err);
      }
    }
    loadPrompts();

    // Initial greeting message
    const initialGreeting: ChatMessageUI = {
      id: 'greeting-1',
      role: 'assistant',
      content: language === 'te'
        ? `నమస్తే! నేను మెడ్‌మైండ్ AI క్లినికల్ అసిస్టెంట్‌ని. హెమటాలజీ, FBC విశ్లేషణ, మైక్రోసైటిక్/మాక్రోసైటిక్ అవకలన రోగనిర్ధారణలు మరియు క్లినికల్ తార్కిక ప్రశ్నలకు సహాయం చేయడానికి నేను ఇక్కడ ఉన్నాను. మీరు ఏదైనా ప్రశ్న అడగవచ్చు లేదా దిగువ ప్రశ్నలను ఎంచుకోవచ్చు!`
        : `Hello! I'm your MedMind AI Clinical Reasoning Assistant. I can help you systematically read full blood counts, differentiate challenging anemias (such as iron deficiency vs thalassemia trait, or ferritin in inflammation), explain diagnostic algorithms, and coach your clinical reasoning.

Select any starter inquiry below or type a custom haematology question to begin!`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      model: 'MedMind Clinical Knowledge Engine',
      suggested_questions: [
        'How do I systematically read a full blood count step-by-step?',
        'How do I distinguish iron deficiency from beta-thalassaemia trait?',
        'Why can serum ferritin be normal or high even when a patient is iron deficient?',
        'What are the red flag symptoms in unexplained anaemia requiring senior escalation?'
      ]
    };
    setMessages([initialGreeting]);
  }, [language]);

  // Scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputMessage).trim();
    if (!query || loading) return;

    const userMsg: ChatMessageUI = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      // Build history for backend
      const history = messages.slice(-6).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const contextData: Record<string, any> = {};
      if (caseContextId) contextData.case_id = caseContextId;
      if (lessonContextId) contextData.lesson_id = lessonContextId;

      const res = await api.assistant.chat({
        message: query,
        context: Object.keys(contextData).length > 0 ? contextData : undefined,
        history,
      });

      const assistantMsg: ChatMessageUI = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: res.reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        citations: res.citations || [],
        suggested_questions: res.suggested_questions || [],
        recommended_lessons: res.recommended_lessons || [],
        model: res.model || 'MedMind AI',
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessageUI = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: `I encountered an issue processing your query: ${err.message || 'Network error'}. Please try asking again.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 'reset-greeting',
        role: 'assistant',
        content: 'Conversation history reset. How can I assist your clinical reasoning today?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        suggested_questions: [
          'How do I systematically read a full blood count step-by-step?',
          'How do I distinguish iron deficiency from beta-thalassaemia trait?',
          'What are red-flag features in unexplained anaemia?'
        ]
      }
    ]);
  };

  const allPrompts = promptGroups.flatMap((g) => g.prompts);
  const activePrompts =
    selectedCategory === 'all'
      ? allPrompts.slice(0, 6)
      : promptGroups.find((g) => g.category === selectedCategory)?.prompts || [];

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 space-y-6">
      {/* Header & Badges */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-100 text-purple-800 border border-purple-200">
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              <span>Grounded AI Clinical Mentor</span>
            </span>
            {caseContextId && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200">
                <Stethoscope className="w-3 h-3 text-blue-600" />
                <span>Case Context: {caseContextId}</span>
              </span>
            )}
            {lessonContextId && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                <GraduationCap className="w-3 h-3 text-emerald-600" />
                <span>Lesson Context: {lessonContextId}</span>
              </span>
            )}
          </div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            MEDMIND AI Clinical Reasoning Assistant
          </h1>
          <p className="text-sm text-slate-600 mt-0.5">
            Grounded diagnostic reasoning, haematology algorithms, and evidence coaching for trainees.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleClearChat}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Chat</span>
          </button>
          <Link
            to="/lessons"
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-medblue-600 text-white text-xs font-bold hover:bg-medblue-700 transition-colors shadow-xs"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Practice Lessons</span>
          </Link>
        </div>
      </div>

      {/* Educational Simulation Disclaimer */}
      <div className="bg-amber-50/80 border border-amber-200 rounded-xl p-3.5 text-xs text-amber-900 flex items-start gap-2.5">
        <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <strong>Educational Simulation Simulator Only:</strong> This AI tutor is strictly intended for clinical problem-solving practice and healthcare training with fictional cases. It does not provide medical advice or real-patient prescribing doses. Standard adult reference ranges vary between laboratories.
        </div>
      </div>

      {/* Main Layout: Left/Top Starter Questions + Main Chat Thread */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Column: Topic Categories & Quick Prompts */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-medblue-600" />
              <span>Diagnostic Domains</span>
            </h3>

            <div className="flex flex-col gap-1">
              <button
                onClick={() => setSelectedCategory('all')}
                className={`text-left text-xs font-semibold px-3 py-2 rounded-lg transition-colors ${
                  selectedCategory === 'all'
                    ? 'bg-medblue-50 text-medblue-700 font-bold'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`}
              >
                All Key Domains
              </button>
              {promptGroups.map((g) => (
                <button
                  key={g.category}
                  onClick={() => setSelectedCategory(g.category)}
                  className={`text-left text-xs font-semibold px-3 py-2 rounded-lg transition-colors ${
                    selectedCategory === g.category
                      ? 'bg-medblue-50 text-medblue-700 font-bold'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  }`}
                >
                  {g.category}
                </button>
              ))}
            </div>
          </div>

          {/* Quick Click Prompts */}
          <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs space-y-2.5">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              High-Yield Clinical Prompts
            </h3>
            <p className="text-[11px] text-slate-500">
              Click any clinical inquiry below to send it to the assistant:
            </p>

            <div className="space-y-2">
              {activePrompts.map((promptText, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(promptText)}
                  className="w-full text-left text-xs p-2.5 rounded-xl border border-slate-200 hover:border-medblue-400 hover:bg-medblue-50/50 text-slate-700 hover:text-medblue-900 transition-all leading-snug group flex items-start gap-1.5"
                >
                  <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-medblue-600 shrink-0 mt-0.5" />
                  <span>{promptText}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Columns: Interactive Chat Canvas */}
        <div className="lg:col-span-3 flex flex-col bg-white rounded-2xl border border-slate-200 shadow-xs h-[720px] overflow-hidden">
          {/* Chat Messages Scrollable Box */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'assistant' && (
                  <div className="w-9 h-9 rounded-xl bg-purple-100 border border-purple-200 flex items-center justify-center text-purple-700 shrink-0 mt-1 shadow-xs">
                    <Bot className="w-5 h-5" />
                  </div>
                )}

                <div
                  className={`max-w-[85%] rounded-2xl p-4 sm:p-5 shadow-xs ${
                    msg.role === 'user'
                      ? 'bg-medblue-600 text-white rounded-br-xs'
                      : 'bg-slate-50 border border-slate-200/80 text-slate-800 rounded-bl-xs space-y-4'
                  }`}
                >
                  {/* Sender & Timestamp */}
                  <div className="flex items-center justify-between gap-4 text-[11px] opacity-75 mb-1">
                    <span className="font-bold">
                      {msg.role === 'user' ? user?.display_name || 'Medical Student' : 'MedMind Clinical Tutor'}
                    </span>
                    <span>{msg.timestamp}</span>
                  </div>

                  {/* Body Text */}
                  <div className="text-sm leading-relaxed whitespace-pre-line space-y-2">
                    {msg.content}
                  </div>

                  {/* Assistant Citations & References */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="pt-3 border-t border-slate-200/60 space-y-2">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                        Grounded Reference Excerpts:
                      </span>
                      <div className="flex flex-wrap gap-2">
                        {msg.citations.map((c, i) => (
                          <button
                            key={i}
                            onClick={() => setSelectedCitation(c)}
                            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:border-medblue-500 hover:text-medblue-700 hover:bg-medblue-50 transition-colors shadow-2xs"
                          >
                            <BookOpen className="w-3 h-3 text-medblue-600" />
                            <span>{c.ref_id}</span>
                            <span className="text-[10px] text-slate-400 font-normal truncate max-w-[140px]">
                              {c.source_title}
                            </span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Recommended Practice Lessons */}
                  {msg.recommended_lessons && msg.recommended_lessons.length > 0 && (
                    <div className="pt-3 border-t border-slate-200/60 space-y-2">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                        Recommended Practice Modules:
                      </span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {msg.recommended_lessons.map((lesson) => (
                          <Link
                            key={lesson.id}
                            to={`/lesson/${lesson.id}`}
                            className="p-2.5 rounded-xl bg-white border border-slate-200 hover:border-emerald-400 hover:bg-emerald-50/40 text-slate-800 transition-all flex items-center justify-between group shadow-2xs"
                          >
                            <div className="flex items-center gap-2 min-w-0">
                              <div className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                                <GraduationCap className="w-3.5 h-3.5" />
                              </div>
                              <div className="min-w-0">
                                <span className="text-[10px] font-mono font-bold text-emerald-700 block">
                                  {lesson.id}
                                </span>
                                <span className="text-xs font-semibold text-slate-700 group-hover:text-emerald-800 truncate block">
                                  {lesson.title}
                                </span>
                              </div>
                            </div>
                            <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-emerald-600 shrink-0 ml-1" />
                          </Link>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Suggested Follow-up Questions */}
                  {msg.suggested_questions && msg.suggested_questions.length > 0 && (
                    <div className="pt-3 border-t border-slate-200/60 space-y-2">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                        Suggested Follow-Up Reasoning:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {msg.suggested_questions.map((qText, qi) => (
                          <button
                            key={qi}
                            onClick={() => handleSendMessage(qText)}
                            className="text-left text-xs px-2.5 py-1 rounded-full bg-white border border-purple-200 text-purple-900 hover:bg-purple-50 transition-colors shadow-2xs"
                          >
                            • {qText}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Model engine tag */}
                  {msg.model && (
                    <div className="text-[10px] text-slate-400 font-mono text-right pt-1">
                      Engine: {msg.model}
                    </div>
                  )}
                </div>

                {msg.role === 'user' && (
                  <div className="w-9 h-9 rounded-xl bg-medblue-600 flex items-center justify-center text-white shrink-0 mt-1 shadow-xs">
                    <UserIcon className="w-5 h-5" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3 justify-start">
                <div className="w-9 h-9 rounded-xl bg-purple-100 border border-purple-200 flex items-center justify-center text-purple-700 shrink-0 shadow-xs">
                  <Bot className="w-5 h-5 animate-pulse" />
                </div>
                <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 shadow-xs flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce" />
                  <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce [animation-delay:0.2s]" />
                  <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce [animation-delay:0.4s]" />
                  <span className="text-xs font-semibold text-slate-500 ml-1">
                    Analyzing clinical findings & synthesizing grounded guidance...
                  </span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input Bar */}
          <div className="p-4 border-t border-slate-200 bg-slate-50/50">
            <div className="flex items-end gap-2 bg-white rounded-xl border border-slate-300 p-2 shadow-inner focus-within:border-medblue-500 focus-within:ring-2 focus-within:ring-medblue-200 transition-all">
              <textarea
                ref={inputRef}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about FBC indices, iron vs thalassaemia, ferritin confounders, macrocytic workups, or red flags..."
                className="flex-1 max-h-32 min-h-[44px] p-1.5 text-sm text-slate-800 placeholder-slate-400 bg-transparent resize-none focus:outline-none"
                rows={1}
              />
              <button
                onClick={() => handleSendMessage()}
                disabled={!inputMessage.trim() || loading}
                className="p-2.5 rounded-lg bg-medblue-600 text-white hover:bg-medblue-700 disabled:opacity-40 disabled:hover:bg-medblue-600 transition-colors shadow-xs shrink-0"
                title="Send message (Enter)"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-500 px-1 mt-1.5">
              <span>Press <strong className="font-semibold text-slate-700">Enter</strong> to send, <strong className="font-semibold text-slate-700">Shift + Enter</strong> for a new line</span>
              <span className="italic">Grounded on WHO, BSH & StatPearls references</span>
            </div>
          </div>
        </div>
      </div>

      {/* Citation Popover Modal */}
      {selectedCitation && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-xl border border-slate-200">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[11px] font-mono font-bold text-medblue-600 uppercase tracking-wider block">
                  Reference Evidence Detail
                </span>
                <h3 className="text-base font-bold text-slate-900">
                  {selectedCitation.source_title}
                </h3>
              </div>
              <button
                onClick={() => setSelectedCitation(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 space-y-2">
              <div className="flex items-center gap-1.5 font-bold text-slate-900">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Reference ID: {selectedCitation.ref_id}</span>
              </div>
              {selectedCitation.relevance && (
                <p>
                  <strong>Clinical Relevance:</strong> {selectedCitation.relevance}
                </p>
              )}
              {selectedCitation.quote && (
                <blockquote className="italic border-l-2 border-medblue-500 pl-2 text-slate-600">
                  "{selectedCitation.quote}"
                </blockquote>
              )}
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setSelectedCitation(null)}
                className="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 font-semibold text-xs"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
