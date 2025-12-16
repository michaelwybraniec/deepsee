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
            <Link to="/tasks" className="flex items-center gap-2 text-xl font-bold text-gray-900 hover:text-blue-500 transition-colors">
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
                className="px-3 py-1.5 bg-gray-100 text-gray-700 font-medium rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                Change Password
              </Link>
              <button
                onClick={handleLogout}
                className="px-3 py-1.5 bg-blue-500 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                Logout
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
