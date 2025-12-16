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

  const formatDateShort = (dateString) => {
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
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{task.title}</h1>
        <div className="flex flex-wrap gap-2">
          {isOwner && (
            <>
              <Link
                to={`/tasks/${task.id}/edit`}
                className="px-5 py-2.5 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                Edit
              </Link>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="px-5 py-2.5 bg-red-600 text-white font-medium rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {deleting ? 'Deleting...' : 'Delete'}
              </button>
            </>
          )}
          <Link
            to="/tasks"
            className="px-5 py-2.5 bg-gray-200 text-gray-700 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
          >
            Back
          </Link>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <div className="text-sm text-red-800 font-medium">{error}</div>
        </div>
      )}

      {/* Single Card Layout */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6 space-y-6">
        {task.description && (
          <div>
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Description</h2>
            <p className="text-base text-gray-900 whitespace-pre-wrap leading-relaxed">
              {task.description}
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Status</dt>
            <dd>
              {task.status ? (
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
                  {task.status}
                </span>
              ) : (
                <span className="text-base font-medium text-gray-900">Not set</span>
              )}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Priority</dt>
            <dd>
              {task.priority ? (
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
              ) : (
                <span className="text-base font-medium text-gray-900">Not set</span>
              )}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Due Date</dt>
            <dd className="text-base font-medium text-gray-900">
              {formatDateShort(task.due_date)}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Tags</dt>
            <dd className="text-base font-medium text-gray-900">
              {task.tags && task.tags.length > 0 ? task.tags.join(', ') : 'No tags'}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Created</dt>
            <dd className="text-sm text-gray-600">
              {formatDate(task.created_at)}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Last Updated</dt>
            <dd className="text-sm text-gray-600">
              {formatDate(task.updated_at)}
            </dd>
          </div>
        </div>

        {/* Attachments inside the card */}
        <div className="border-t border-gray-200 pt-6">
          <AttachmentsSection taskId={task.id} isOwner={isOwner} />
        </div>
      </div>
    </div>
  );
}

export default TaskDetailPage;
