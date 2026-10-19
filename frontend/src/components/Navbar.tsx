import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Activity, Languages, LogOut, User, BarChart2, BookOpen, GraduationCap, Shield } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'te' : 'en');
  };

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center gap-8">
            <Link to="/cases" className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-xl bg-medblue-600 flex items-center justify-center text-white shadow-md shadow-medblue-500/20">
                <Activity className="w-6 h-6 stroke-[2.5]" />
              </div>
              <div>
                <span className="text-xl font-black tracking-tight text-slate-900 block leading-tight">
                  MEDMIND <span className="text-medblue-600">AI</span>
                </span>
                <span className="text-[10px] font-semibold tracking-wider text-slate-600 uppercase block -mt-0.5">
                  Clinical Simulator 2.0
                </span>
              </div>
            </Link>

            {user && (
              <div className="hidden md:flex items-center gap-1">
                <Link
                  to="/cases"
                  className={`px-3 py-2 rounded-lg text-sm font-semibold transition-colors flex items-center gap-1.5 ${
                    location.pathname.startsWith('/cases') || location.pathname.startsWith('/attempt')
                      ? 'bg-medblue-50 text-medblue-700'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <BookOpen className="w-4 h-4" />
                  <span>{t.nav.cases}</span>
                </Link>

                <Link
                  to="/progress"
                  className={`px-3 py-2 rounded-lg text-sm font-semibold transition-colors flex items-center gap-1.5 ${
                    location.pathname === '/progress'
                      ? 'bg-medblue-50 text-medblue-700'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <BarChart2 className="w-4 h-4" />
                  <span>{t.nav.progress}</span>
                </Link>

                {user.role === 'teacher' && (
                  <Link
                    to="/teacher"
                    className={`px-3 py-2 rounded-lg text-sm font-semibold transition-colors flex items-center gap-1.5 ${
                      location.pathname === '/teacher'
                        ? 'bg-medblue-50 text-medblue-700'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }`}
                  >
                    <GraduationCap className="w-4 h-4" />
                    <span>{t.nav.teacher}</span>
                  </Link>
                )}
              </div>
            )}
          </div>

          <div className="flex items-center gap-3">
            {/* Language Switcher */}
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
              title="Switch Language / భాషను మార్చండి"
            >
              <Languages className="w-4 h-4 text-medblue-600" />
              <span>{language === 'en' ? 'తెలుగు' : 'English'}</span>
            </button>

            {user ? (
              <div className="flex items-center gap-3 pl-2 border-l border-slate-200">
                <div className="hidden sm:block text-right">
                  <div className="text-xs font-bold text-slate-900 leading-tight">
                    {user.display_name}
                  </div>
                  <div className="text-[10px] font-semibold text-slate-600 flex items-center justify-end gap-1">
                    {user.role === 'teacher' ? (
                      <span className="bg-purple-100 text-purple-800 px-1.5 py-0.2 rounded font-bold">
                        Faculty
                      </span>
                    ) : (
                      <span className="bg-blue-100 text-blue-800 px-1.5 py-0.2 rounded font-bold">
                        Student
                      </span>
                    )}
                  </div>
                </div>

                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  title={t.nav.logout}
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="bg-medblue-600 hover:bg-medblue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors shadow-sm"
              >
                {t.login.signInBtn}
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
