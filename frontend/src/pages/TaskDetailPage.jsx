import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { toast } from 'sonner';
import { getTask, deleteTask } from '../services/taskApi';
import { useAuth } from '../contexts/AuthContext';
import AttachmentsSection from '../components/AttachmentsSection';

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
      toast.success('Task deleted successfully!');
      navigate('/tasks');
    } else {
      const errorMsg = result.error || 'Failed to delete task';
      setError(errorMsg);
      toast.error(errorMsg);
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
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading task...</div>
      </div>
    );
  }

  if (error && !task) {
    return (
      <div className="bg-red-50 border border-red-200 rounded p-4">
        <div className="text-sm text-red-800 mb-2">{error}</div>
        <button
          onClick={() => navigate('/tasks')}
          className="text-sm text-red-600 hover:text-red-800 underline"
        >
          Back to tasks
        </button>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 mb-4">Task not found.</p>
        <Link
          to="/tasks"
          className="text-blue-600 hover:text-blue-800 underline"
        >
          Back to tasks
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 mb-4">
        <h1 className="text-2xl font-semibold text-gray-900">{task.title}</h1>
        <div className="flex flex-wrap gap-2">
          {isOwner && (
            <>
              <Link
                to={`/tasks/${task.id}/edit`}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm font-medium"
              >
                Edit
              </Link>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
              >
                {deleting ? 'Deleting...' : 'Delete'}
              </button>
            </>
          )}
          <Link
            to="/tasks"
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 text-sm font-medium"
          >
            Back
          </Link>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-4 mb-4">
          <div className="text-sm text-red-800">{error}</div>
        </div>
      )}

      <div className="border border-gray-200 rounded p-4 mb-4">
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <dt className="text-sm font-medium text-gray-500 mb-1">Status</dt>
            <dd className="text-sm text-gray-900">
              {task.status || 'Not set'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 mb-1">Priority</dt>
            <dd className="text-sm text-gray-900">
              {task.priority || 'Not set'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 mb-1">Due Date</dt>
            <dd className="text-sm text-gray-900">
              {formatDate(task.due_date)}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 mb-1">Tags</dt>
            <dd className="text-sm text-gray-900">
              {task.tags && task.tags.length > 0 ? task.tags.join(', ') : 'No tags'}
            </dd>
          </div>
          <div className="sm:col-span-2">
            <dt className="text-sm font-medium text-gray-500 mb-1">Description</dt>
            <dd className="text-sm text-gray-900 whitespace-pre-wrap">
              {task.description || 'No description'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 mb-1">Created</dt>
            <dd className="text-sm text-gray-900">
              {formatDate(task.created_at)}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 mb-1">Last Updated</dt>
            <dd className="text-sm text-gray-900">
              {formatDate(task.updated_at)}
            </dd>
          </div>
        </dl>
      </div>

      <div className="mt-4">
        <AttachmentsSection taskId={task.id} isOwner={isOwner} />
      </div>
    </div>
  );
}

export default TaskDetailPage;
