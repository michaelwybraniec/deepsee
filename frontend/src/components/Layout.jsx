import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Layout() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-white">
      <nav className="border-b border-gray-200">
        <div className="px-4">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center py-3 gap-3">
            <Link to="/tasks" className="text-lg font-semibold text-gray-900">
              Task Tracker
            </Link>
            <div className="flex flex-wrap items-center gap-2 sm:gap-4 text-sm">
              {user && (
                <span className="text-gray-600">
                  {user.username || user.email}
                </span>
              )}
              <Link
                to="/change-password"
                className="text-gray-600 hover:text-gray-900"
              >
                Change Password
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="px-4 py-4 sm:px-6 sm:py-6">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
