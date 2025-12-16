import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getTask, deleteTask } from '../services/taskApi';
import { useAuth } from '../contexts/AuthContext';

function TaskDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchTask();
  }, [id]);

  const fetchTask = async () => {
    setLoading(true);
    setError('');
    const result = await getTask(id);
    
    if (result.success) {
      setTask(result.data);
    } else {
      setError(result.error || 'Failed to load task');
    }
    setLoading(false);
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setDeleting(true);
    const result = await deleteTask(id);
    
    if (result.success) {
      navigate('/tasks');
    } else {
      setError(result.error || 'Failed to delete task');
      setDeleting(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const isOwner = task && user && task.owner_user_id === user.id;

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading task...</div>
      </div>
    );
  }

  if (error && !task) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="text-sm text-red-800">{error}</div>
        <button
          onClick={() => navigate('/tasks')}
          className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
        >
          Back to tasks
        </button>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Task not found.</p>
        <Link
          to="/tasks"
          className="mt-4 text-indigo-600 hover:text-indigo-800 underline"
        >
          Back to tasks
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{task.title}</h1>
        <div className="flex space-x-2">
          {isOwner && (
            <>
              <Link
                to={`/tasks/${task.id}/edit`}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Edit
              </Link>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {deleting ? 'Deleting...' : 'Delete'}
              </button>
            </>
          )}
          <Link
            to="/tasks"
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Back
          </Link>
        </div>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4 mb-4">
          <div className="text-sm text-red-800">{error}</div>
        </div>
      )}

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
            <div>
              <dt className="text-sm font-medium text-gray-500">Status</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {task.status || 'Not set'}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Priority</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {task.priority || 'Not set'}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Due Date</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {formatDate(task.due_date)}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Tags</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {task.tags && task.tags.length > 0 ? task.tags.join(', ') : 'No tags'}
              </dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-sm font-medium text-gray-500">Description</dt>
              <dd className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">
                {task.description || 'No description'}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Created</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {formatDate(task.created_at)}
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {formatDate(task.updated_at)}
              </dd>
            </div>
          </dl>
        </div>
      </div>

      {/* Attachments section will be implemented in task 10.5 */}
      <div className="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h2 className="text-lg font-medium text-gray-900">Attachments</h2>
          <p className="mt-2 text-sm text-gray-500">
            Attachments section will be implemented in task 10.5
          </p>
        </div>
      </div>
    </div>
  );
}

export default TaskDetailPage;
