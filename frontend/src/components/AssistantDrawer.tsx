import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Sparkles,
  X,
  Send,
  Bot,
  User,
  BookOpen,
  ChevronUp,
  RotateCcw,
  AlertCircle,
  HelpCircle,
  Maximize2
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';
import { ChatMessageUI, AssistantCitation } from '../types';

export const AssistantDrawer: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessageUI[]>([
    {
      id: 'drawer-welcome',
      role: 'assistant',
      content: 'Need help interpreting an FBC panel, sorting out a differential, or evaluating ferritin in inflammation? Ask me anytime!',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      suggested_questions: [
        'How do I tell iron deficiency from thalassaemia?',
        'Why can ferritin be normal in anaemia?'
      ]
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const location = useLocation();

  // Extract case or lesson ID if on attempt or lesson page
  const isAttemptPage = location.pathname.startsWith('/attempt/');
  const isLessonPage = location.pathname.startsWith('/lesson/');

  // Don't show drawer if on /assistant page itself to avoid duplication
  const isOnAssistantPage = location.pathname === '/assistant';

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, loading]);

  const handleSendMessage = async (customQuery?: string) => {
    const query = (customQuery || inputMessage).trim();
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
      const history = messages.slice(-4).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const contextData: Record<string, any> = { current_path: location.pathname };

      const res = await api.assistant.chat({
        message: query,
        context: contextData,
        history,
      });

      const assistantMsg: ChatMessageUI = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: res.reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        citations: res.citations || [],
        suggested_questions: res.suggested_questions || [],
        model: res.model,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: `Assistant error: ${err.message || 'Network issue'}.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (isOnAssistantPage) return null;

  return (
    <>
      {/* Floating Trigger Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-5 right-5 z-40 flex items-center gap-2 px-4 py-2.5 rounded-full bg-gradient-to-r from-purple-600 to-medblue-600 text-white font-bold text-xs shadow-lg shadow-purple-600/30 hover:shadow-xl hover:scale-105 active:scale-95 transition-all group"
          title="Open MedMind AI Clinical Assistant"
        >
          <Sparkles className="w-4 h-4 text-purple-200 group-hover:rotate-12 transition-transform" />
          <span>AI Clinical Mentor</span>
          {(isAttemptPage || isLessonPage) && (
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          )}
        </button>
      )}

      {/* Slide-over Drawer Window */}
      {isOpen && (
        <div className="fixed bottom-5 right-5 z-40 w-96 max-w-[calc(100vw-2.5rem)] h-[560px] max-h-[calc(100vh-3rem)] bg-white rounded-2xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-200">
          {/* Drawer Header */}
          <div className="px-4 py-3 bg-slate-900 text-white flex items-center justify-between shrink-0">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-purple-500/20 border border-purple-400/30 flex items-center justify-center text-purple-300">
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <span className="text-xs font-bold block leading-tight">AI Clinical Assistant</span>
                <span className="text-[10px] text-slate-400 block -mt-0.5">Evidence Grounded Coach</span>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <Link
                to="/assistant"
                target="_blank"
                rel="noreferrer"
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
                title="Open full page assistant in new tab"
              >
                <Maximize2 className="w-3.5 h-3.5" />
              </Link>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
                title="Close drawer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Educational notice */}
          <div className="px-3 py-1.5 bg-amber-50 border-b border-amber-100 text-[10px] text-amber-800 flex items-center gap-1.5 shrink-0">
            <AlertCircle className="w-3 h-3 text-amber-600 shrink-0" />
            <span className="truncate">Simulation tutor · Fictional educational use only</span>
          </div>

          {/* Messages scroll box */}
          <div className="flex-1 overflow-y-auto p-3 space-y-3 bg-slate-50">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex gap-2 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {m.role === 'assistant' && (
                  <div className="w-6 h-6 rounded-md bg-purple-100 border border-purple-200 text-purple-700 flex items-center justify-center shrink-0 mt-0.5">
                    <Bot className="w-3.5 h-3.5" />
                  </div>
                )}
                <div
                  className={`max-w-[85%] rounded-xl p-3 text-xs leading-relaxed ${
                    m.role === 'user'
                      ? 'bg-medblue-600 text-white rounded-br-none'
                      : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none shadow-2xs space-y-2'
                  }`}
                >
                  <div className="whitespace-pre-line">{m.content}</div>

                  {/* Citations */}
                  {m.citations && m.citations.length > 0 && (
                    <div className="pt-2 border-t border-slate-100 flex flex-wrap gap-1">
                      {m.citations.map((c, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] bg-slate-100 text-slate-600 font-mono font-semibold"
                        >
                          <BookOpen className="w-2.5 h-2.5 text-medblue-600" />
                          <span>{c.ref_id}</span>
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Suggested questions */}
                  {m.suggested_questions && m.suggested_questions.length > 0 && (
                    <div className="pt-2 border-t border-slate-100 space-y-1">
                      {m.suggested_questions.map((qText, qi) => (
                        <button
                          key={qi}
                          onClick={() => handleSendMessage(qText)}
                          className="w-full text-left text-[11px] p-1 rounded hover:bg-purple-50 text-purple-800 transition-colors block truncate"
                        >
                          • {qText}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex gap-2 items-center text-xs text-slate-400 p-2">
                <div className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-bounce" />
                <div className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-bounce [animation-delay:0.2s]" />
                <div className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-bounce [animation-delay:0.4s]" />
                <span className="text-[11px] ml-1">Thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick prompt chips */}
          <div className="p-2 border-t border-slate-200 bg-white space-y-1.5">
            <div className="flex items-center justify-between text-[10px] text-slate-500">
              <span className="font-semibold">Quick Prompts:</span>
              <button
                onClick={() =>
                  setMessages([
                    {
                      id: 'reset',
                      role: 'assistant',
                      content: 'Chat cleared. How can I help with your clinical reasoning?',
                      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    }
                  ])
                }
                className="hover:text-slate-800"
              >
                Clear
              </button>
            </div>
            <div className="flex gap-1 overflow-x-auto pb-1 text-[11px]">
              <button
                onClick={() => handleSendMessage('How do I systematically read an FBC?')}
                className="whitespace-nowrap px-2 py-1 rounded-md bg-slate-100 text-slate-700 hover:bg-slate-200"
              >
                FBC Steps
              </button>
              <button
                onClick={() => handleSendMessage('Explain ferritin as an acute-phase reactant')}
                className="whitespace-nowrap px-2 py-1 rounded-md bg-slate-100 text-slate-700 hover:bg-slate-200"
              >
                Ferritin Confounders
              </button>
              <button
                onClick={() => handleSendMessage('What are red flags in older adults with anaemia?')}
                className="whitespace-nowrap px-2 py-1 rounded-md bg-slate-100 text-slate-700 hover:bg-slate-200"
              >
                Red Flags
              </button>
            </div>

            {/* Input Bar */}
            <div className="flex items-center gap-1.5 pt-1">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleSendMessage();
                  }
                }}
                placeholder="Ask clinical assistant..."
                className="flex-1 px-3 py-1.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:border-medblue-500"
              />
              <button
                onClick={() => handleSendMessage()}
                disabled={!inputMessage.trim() || loading}
                className="p-1.5 rounded-lg bg-medblue-600 text-white disabled:opacity-40 hover:bg-medblue-700"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
