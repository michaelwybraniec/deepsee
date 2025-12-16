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
            <Link to="/tasks" className="text-xl font-bold text-gray-900 hover:text-blue-600 transition-colors">
              Task Tracker
            </Link>
            <div className="flex flex-wrap items-center gap-3 sm:gap-4 text-sm">
              {user && (
                <span className="text-gray-700 font-medium">
                  {user.username || user.email}
                </span>
              )}
              <Link
                to="/change-password"
                className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
              >
                Change Password
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
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
