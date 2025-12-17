import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'sonner';
import { useAuth } from '../contexts/useAuth';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Client-side validation
    if (!username.trim()) {
      toast.error('Username is required');
      setLoading(false);
      return;
    }

    if (!password) {
      toast.error('Password is required');
      setLoading(false);
      return;
    }

    try {
      const result = await login(username.trim(), password);

      if (result.success) {
        toast.success('Login successful!');
        // Redirect to task list on success
        navigate('/tasks');
      } else {
        // Ensure error is always a string
        let errorMsg = 'Login failed. Please check your credentials.';
        if (result.error) {
          if (typeof result.error === 'string') {
            errorMsg = result.error;
          } else if (result.error.message) {
            errorMsg = result.error.message;
          } else {
            errorMsg = JSON.stringify(result.error);
          }
        }
        toast.error(errorMsg);
      }
    } catch (err) {
      toast.error('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-md p-8 space-y-6">
        <div className="text-center">
          <div className="flex items-center justify-center gap-3 mb-2">
            <img src="/favicon.svg" alt="Task Tracker" className="h-12 w-12" />
            <h1 className="text-3xl font-bold text-gray-900">
              Task Tracker
            </h1>
          </div>
        </div>
        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="username" className="sr-only">
              Username
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              className="w-full px-4 py-2.5 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-shadow"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={loading}
            />
          </div>
          <div>
            <label htmlFor="password" className="sr-only">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="w-full px-4 py-2.5 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-shadow"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-primary-500 text-white font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            style={{ backgroundColor: '#3b82f6' }}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div className="text-center text-sm">
          <span className="text-gray-600">Don't have an account? </span>
          <Link to="/register" className="text-primary-500 hover:text-primary-700 font-medium">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
