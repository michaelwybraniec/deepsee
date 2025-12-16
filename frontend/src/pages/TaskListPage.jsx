import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getTasks } from '../services/taskApi';

function TaskListPage() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setLoading(true);
    setError('');
    const result = await getTasks();
    
    if (result.success) {
      // API returns { tasks: [], pagination: {} }
      setTasks(result.data.tasks || result.data.items || []);
    } else {
      setError(result.error || 'Failed to load tasks');
    }
    setLoading(false);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'done':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'todo':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading tasks...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded p-4">
        <div className="text-sm text-red-800 mb-2">{error}</div>
        <button
          onClick={fetchTasks}
          className="text-sm text-red-600 hover:text-red-800 underline"
        >
          Try again
        </button>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-4 sm:mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Tasks</h1>
        <Link
          to="/tasks/new"
          className="px-4 py-2 sm:px-5 sm:py-2.5 bg-blue-600 text-white text-sm sm:text-base font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors inline-flex items-center justify-center"
        >
          Create Task
        </Link>
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-12 sm:py-16 bg-white rounded-lg border border-gray-200 px-4">
          <p className="text-gray-600 mb-3 sm:mb-4 text-base sm:text-lg">No tasks found.</p>
          <Link
            to="/tasks/new"
            className="text-blue-600 hover:text-blue-700 font-medium underline text-sm sm:text-base"
          >
            Create your first task
          </Link>
        </div>
      ) : (
        <div className="space-y-2 sm:space-y-3">
          {tasks.map((task) => (
            <div
              key={task.id}
              onClick={() => navigate(`/tasks/${task.id}`)}
              className="block hover:bg-gray-50 active:bg-gray-100 cursor-pointer bg-white rounded-lg border border-gray-200 p-3 sm:p-4 transition-colors"
            >
              <div className="flex items-start justify-between gap-2 sm:gap-3">
                {/* Main Content */}
                <div className="flex-1 min-w-0 space-y-1 sm:space-y-1.5">
                  {/* Title Row */}
                  <div className="flex flex-col sm:flex-row sm:items-start gap-1.5 sm:gap-2">
                    <h3 className="text-base sm:text-lg font-semibold text-gray-900 flex-1 leading-tight">
                      {task.title}
                    </h3>
                    {/* Status and Priority - Wrap on mobile */}
                    <div className="flex items-center gap-1.5 flex-shrink-0 flex-wrap">
                      {task.status && (
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}
                        >
                          {task.status}
                        </span>
                      )}
                      {task.priority && (
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}
                        >
                          {task.priority}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Description */}
                  {task.description && (
                    <p className="text-sm text-gray-600 line-clamp-2 leading-relaxed">
                      {task.description}
                    </p>
                  )}

                  {/* Metadata Row */}
                  <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                      <svg className="h-3 w-3 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span className="font-medium text-gray-700">{formatDate(task.due_date)}</span>
                    </div>
                    {task.tags && task.tags.length > 0 && (
                      <div className="flex items-center gap-1 min-w-0">
                        <svg className="h-3 w-3 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                        </svg>
                        <span className="truncate">{task.tags.join(', ')}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Arrow Icon - Better touch target on mobile */}
                <svg
                  className="h-5 w-5 sm:h-4 sm:w-4 text-gray-400 flex-shrink-0 mt-0.5 sm:mt-1"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TaskListPage;
