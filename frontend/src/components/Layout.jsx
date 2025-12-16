import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Layout() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center py-4 gap-3">
            <Link to="/tasks" className="flex items-center gap-2 text-xl font-bold text-gray-900 hover:text-primary-500 transition-colors">
              <img src="/favicon.svg" alt="Task Tracker" className="h-8 w-8" />
              Task Tracker
            </Link>
            <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-sm">
              {user && (
                <span className="text-gray-700 font-medium px-2">
                  Hello {user.username || user.email} !
                </span>
              )}
              <Link
                to="/change-password"
                title="Change Password"
                className="p-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
              </Link>
              <button
                onClick={handleLogout}
                title="Logout"
                className="p-2 bg-primary-500 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
                style={{ backgroundColor: '#3b82f6' }}
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="px-4 py-6 sm:px-6 sm:py-8 max-w-7xl mx-auto">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
