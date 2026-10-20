import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, ShieldCheck, UserCheck, GraduationCap, ArrowRight, AlertOctagon, RefreshCw } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { api, BackendUnavailableError } from '../api/client';

export const LoginPage: React.FC = () => {
  const { login, quickLogin } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();

  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [role, setRole] = useState<'student' | 'teacher'>('student');
  const [error, setError] = useState<string | null>(null);
  const [backendDown, setBackendDown] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setBackendDown(false);
    setLoading(true);

    try {
      if (isRegister) {
        const res = await api.auth.register({
          email,
          password,
          display_name: displayName,
          role,
        });
        login(res.access_token, res.user);
      } else {
        const res = await api.auth.login({ email, password });
        login(res.access_token, res.user);
      }
      navigate('/cases');
    } catch (err: any) {
      if (err instanceof BackendUnavailableError || err.name === 'BackendUnavailableError') {
        setBackendDown(true);
      }
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleQuick = async (type: 'student' | 'teacher') => {
    setError(null);
    setBackendDown(false);
    setLoading(true);
    try {
      await quickLogin(type);
      if (type === 'teacher') {
        navigate('/teacher');
      } else {
        navigate('/cases');
      }
    } catch (err: any) {
      if (err instanceof BackendUnavailableError || err.name === 'BackendUnavailableError') {
        setBackendDown(true);
      }
      setError(err.message || 'Quick login failed');
    } finally {
      setLoading(false);
    }
  };

  if (backendDown) {
    return (
      <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full bg-white p-8 rounded-2xl border-2 border-rose-300 shadow-lg text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto">
            <AlertOctagon className="w-9 h-9 stroke-[2.5]" />
          </div>
          <h2 className="text-xl font-black text-slate-900">
            Backend Unavailable
          </h2>
          <p className="text-sm text-slate-600 leading-relaxed font-normal">
            The MEDMIND API service could not be reached. If running locally, ensure the FastAPI server is running with <code className="bg-slate-100 px-1.5 py-0.5 rounded text-xs font-mono font-bold text-slate-800">python run_app.py</code> on port 8000.
          </p>
          <div className="pt-2 flex justify-center gap-3">
            <button
              onClick={() => { setBackendDown(false); setError(null); }}
              className="px-4 py-2 bg-medblue-600 hover:bg-medblue-700 text-white rounded-xl text-xs font-bold flex items-center gap-2 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry Connection</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-6">
        <div className="text-center">
          <div className="w-14 h-14 rounded-2xl bg-medblue-600 flex items-center justify-center text-white mx-auto shadow-lg shadow-medblue-600/30">
            <Activity className="w-8 h-8 stroke-[2.5]" />
          </div>
          <h2 className="mt-4 text-2xl font-black text-slate-900 tracking-tight">
            {t.login.title}
          </h2>
          <p className="mt-1 text-xs text-slate-500">
            {t.login.subtitle}
          </p>
        </div>

        {/* Quick Demo Logins Box */}
        <div className="bg-gradient-to-br from-medblue-50 to-indigo-50 border border-medblue-200/60 rounded-2xl p-5 shadow-xs space-y-3">
          <span className="text-xs font-bold text-medblue-900 uppercase tracking-wider block">
            Documented Demo Credentials
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <button
              type="button"
              onClick={() => handleQuick('student')}
              disabled={loading}
              className="p-3 bg-white hover:bg-slate-50 border border-medblue-200 rounded-xl text-left shadow-xs transition-all flex items-center gap-2.5 group"
            >
              <div className="w-8 h-8 rounded-lg bg-medblue-100 flex items-center justify-center text-medblue-700 shrink-0 group-hover:bg-medblue-600 group-hover:text-white transition-colors">
                <UserCheck className="w-4 h-4" />
              </div>
              <div>
                <span className="text-xs font-bold text-slate-900 block leading-tight">
                  Alex Mercer
                </span>
                <span className="text-[10px] text-slate-500 font-medium">
                  {t.login.roleStudent}
                </span>
              </div>
            </button>

            <button
              type="button"
              onClick={() => handleQuick('teacher')}
              disabled={loading}
              className="p-3 bg-white hover:bg-slate-50 border border-purple-200 rounded-xl text-left shadow-xs transition-all flex items-center gap-2.5 group"
            >
              <div className="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center text-purple-700 shrink-0 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                <GraduationCap className="w-4 h-4" />
              </div>
              <div>
                <span className="text-xs font-bold text-slate-900 block leading-tight">
                  Demo Faculty (placeholder)
                </span>
                <span className="text-[10px] text-slate-500 font-medium">
                  {t.login.roleTeacher}
                </span>
              </div>
            </button>
          </div>
        </div>

        {/* Regular Sign In / Register Form */}
        <div className="bg-white p-7 rounded-2xl border border-slate-200 shadow-xs">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-700 font-medium">
                {error}
              </div>
            )}

            {isRegister && (
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="e.g. Maya Chen"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:border-medblue-500 focus:ring-2 focus:ring-medblue-100 outline-none"
                />
              </div>
            )}

            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">
                {t.login.emailLabel}
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@medmind.ai"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:border-medblue-500 focus:ring-2 focus:ring-medblue-100 outline-none"
              />
            </div>

            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">
                {t.login.passwordLabel}
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:border-medblue-500 focus:ring-2 focus:ring-medblue-100 outline-none"
              />
            </div>

            {isRegister && (
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">
                  Academic Role
                </label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value as any)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:border-medblue-500 outline-none"
                >
                  <option value="student">{t.login.roleStudent}</option>
                  <option value="teacher">{t.login.roleTeacher}</option>
                </select>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl text-sm font-bold text-white bg-medblue-600 hover:bg-medblue-700 transition-all shadow-sm flex items-center justify-center gap-1.5 disabled:opacity-50"
            >
              <span>{isRegister ? 'Create Account' : t.login.signInBtn}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          <div className="mt-4 pt-4 border-t border-slate-100 text-center">
            <button
              type="button"
              onClick={() => setIsRegister(!isRegister)}
              className="text-xs text-medblue-600 hover:text-medblue-800 font-semibold"
            >
              {isRegister ? 'Already have an account? Sign in' : t.login.registerPrompt}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
