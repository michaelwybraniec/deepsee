import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getTasks } from '../services/taskApi';
import { useAuth } from '../contexts/AuthContext';

function TaskListPage() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [initialLoad, setInitialLoad] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { user } = useAuth();

  // Search and filter state
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [tagsFilter, setTagsFilter] = useState('');
  const [dueDateFrom, setDueDateFrom] = useState('');
  const [dueDateTo, setDueDateTo] = useState('');
  const [myTasksFilter, setMyTasksFilter] = useState(false);
  const [sortBy, setSortBy] = useState('created_at:desc');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [pagination, setPagination] = useState(null);

  const fetchTasks = async () => {
    setLoading(true);
    setError('');
    
    const params = {
      page,
      page_size: pageSize,
      sort: sortBy,
    };
    
    if (searchQuery.trim()) {
      params.q = searchQuery.trim();
    }
    if (statusFilter) {
      params.status = statusFilter;
    }
    if (priorityFilter) {
      params.priority = priorityFilter;
    }
    if (tagsFilter.trim()) {
      params.tags = tagsFilter.trim();
    }
    if (dueDateFrom) {
      params.due_date_from = dueDateFrom;
    }
    if (dueDateTo) {
      params.due_date_to = dueDateTo;
    }
    if (myTasksFilter && user?.id) {
      // Ensure owner_user_id is a number (backend expects int)
      params.owner_user_id = Number(user.id);
    }
    
    const result = await getTasks(params);
    
    if (result.success) {
      // API returns { tasks: [], pagination: {} }
      let tasksList = result.data.tasks || result.data.items || [];
      
      setTasks(tasksList);
      
      if (result.data.pagination) {
        setPagination(result.data.pagination);
      } else {
        setPagination(null);
      }
    } else {
      setError(result.error || 'Failed to load tasks');
    }
    setLoading(false);
    setInitialLoad(false);
  };

  // Fetch tasks when filters/page change (debounce search and tags filter)
  useEffect(() => {
    const needsDebounce = searchQuery.trim() || tagsFilter.trim();
    const timeoutId = setTimeout(() => {
      fetchTasks();
    }, needsDebounce ? 500 : 0); // Wait 500ms after user stops typing for search/tags

    return () => clearTimeout(timeoutId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, pageSize, sortBy, statusFilter, priorityFilter, tagsFilter, dueDateFrom, dueDateTo, searchQuery, myTasksFilter, user?.id]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1); // Reset to first page on new search
    fetchTasks(); // Immediate search on button click
  };

  const handleFilterChange = () => {
    setPage(1); // Reset to first page on filter change
  };

  const clearFilters = () => {
    setSearchQuery('');
    setStatusFilter('');
    setPriorityFilter('');
    setTagsFilter('');
    setDueDateFrom('');
    setDueDateTo('');
    setMyTasksFilter(false);
    setSortBy('created_at:desc');
    setPage(1);
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

  // Pagination component
  const PaginationControls = () => {
    if (!pagination || pagination.total_pages <= 1) return null;

    return (
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-sm text-gray-600">
          Showing {((page - 1) * pageSize) + 1} to {Math.min(page * pageSize, pagination.total)} of {pagination.total} tasks
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
            className="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          <div className="flex items-center gap-1">
            {Array.from({ length: Math.min(5, pagination.total_pages) }, (_, i) => {
              let pageNum;
              if (pagination.total_pages <= 5) {
                pageNum = i + 1;
              } else if (page <= 3) {
                pageNum = i + 1;
              } else if (page >= pagination.total_pages - 2) {
                pageNum = pagination.total_pages - 4 + i;
              } else {
                pageNum = page - 2 + i;
              }
              
              return (
                <button
                  key={pageNum}
                  onClick={() => setPage(pageNum)}
                  className={`px-3 py-2 border rounded-md text-sm font-medium ${
                    page === pageNum
                      ? 'bg-primary-500 text-white border-primary-500'
                      : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
                  }`}
                  style={page === pageNum ? { backgroundColor: '#3b82f6' } : {}}
                >
                  {pageNum}
                </button>
              );
            })}
          </div>
          
          <button
            onClick={() => setPage(page + 1)}
            disabled={page === pagination.total_pages}
            className="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-600">Per page:</label>
          <select
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value));
              setPage(1);
            }}
            className="px-2 py-1 bg-white border border-gray-300 rounded-md text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </div>
      </div>
    );
  };

  // Show full loading only on initial load
  if (initialLoad && loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-4 sm:mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Tasks</h1>
        <Link
          to="/tasks/new"
          className="px-4 py-2 sm:px-5 sm:py-2.5 bg-primary-500 text-white text-sm sm:text-base font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors inline-flex items-center justify-center"
          style={{ backgroundColor: '#3b82f6' }}
        >
          Create Task
        </Link>
      </div>

      {/* Search and Filter Section */}
      <div className="mb-4 sm:mb-0">
        {/* Search Bar */}
        <form onSubmit={handleSearch} className="mb-3">
          <div className="flex gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search tasks by title or description..."
              className="flex-1 px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 text-sm font-medium"
              style={{ backgroundColor: '#3b82f6' }}
            >
              Search
            </button>
          </div>
        </form>

        {/* Filters - Always Visible */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {/* Status Filter */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                handleFilterChange();
              }}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
            >
              <option value="">All</option>
              <option value="todo">Todo</option>
              <option value="in_progress">In Progress</option>
              <option value="done">Done</option>
            </select>
          </div>

          {/* Priority Filter */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Priority</label>
            <select
              value={priorityFilter}
              onChange={(e) => {
                setPriorityFilter(e.target.value);
                handleFilterChange();
              }}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
            >
              <option value="">All</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          {/* Tags Filter */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Tags (comma-separated)</label>
            <input
              type="text"
              value={tagsFilter}
              onChange={(e) => {
                setTagsFilter(e.target.value);
                handleFilterChange();
              }}
              placeholder="tag1, tag2"
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
            />
          </div>

          {/* Sort */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value);
                handleFilterChange();
              }}
              className="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
            >
              <option value="created_at:desc">Newest First</option>
              <option value="created_at:asc">Oldest First</option>
              <option value="due_date:asc">Due Date (Ascending)</option>
              <option value="due_date:desc">Due Date (Descending)</option>
              <option value="priority:desc">Priority (High to Low)</option>
              <option value="priority:asc">Priority (Low to High)</option>
              <option value="title:asc">Title (A-Z)</option>
              <option value="title:desc">Title (Z-A)</option>
            </select>
          </div>
        </div>

        {/* Filter Actions */}
        <div className="mt-3 pt-3 border-t border-gray-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={myTasksFilter}
              onChange={(e) => {
                setMyTasksFilter(e.target.checked);
                handleFilterChange();
              }}
              className="w-4 h-4 text-gray-400 bg-white border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-gray-400 accent-gray-400"
            />
            <span className="text-sm text-gray-900">Show only my tasks</span>
          </label>
          {(statusFilter || priorityFilter || tagsFilter || searchQuery || myTasksFilter) && (
            <button
              onClick={clearFilters}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Clear all filters
            </button>
          )}
        </div>
      </div>

      {/* Pagination - Top */}
      <div className="mt-6 mb-4">
        <PaginationControls />
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded p-4">
          <div className="text-sm text-red-800 mb-2">{error}</div>
          <button
            onClick={fetchTasks}
            className="text-sm text-red-600 hover:text-red-800 underline"
          >
            Try again
          </button>
        </div>
      )}

      {/* Task List with Loading Indicator */}
      <div className="relative">
        {loading && !initialLoad && (
          <div className="absolute top-0 left-0 right-0 z-10 bg-white/80 backdrop-blur-sm rounded-lg border border-gray-200 flex items-center justify-center py-8">
            <div className="flex items-center gap-2 text-gray-600">
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span className="text-sm">Loading tasks...</span>
            </div>
          </div>
        )}

        {!loading && tasks.length === 0 ? (
          <div className="text-center py-12 sm:py-16 bg-white rounded-lg border border-gray-200 px-4">
            <p className="text-gray-600 mb-3 sm:mb-4 text-base sm:text-lg">
              {myTasksFilter 
                ? "No tasks found. You don't have any tasks yet." 
                : "No tasks found."}
            </p>
            {!myTasksFilter && (
              <Link
                to="/tasks/new"
                className="text-primary-500 hover:text-primary-700 font-medium underline text-sm sm:text-base"
              >
                Create your first task
              </Link>
            )}
            {myTasksFilter && (
              <div className="space-y-2">
                <p className="text-sm text-gray-500">Try unchecking "Show only my tasks" to see all tasks.</p>
                <Link
                  to="/tasks/new"
                  className="text-primary-500 hover:text-primary-700 font-medium underline text-sm sm:text-base"
                >
                  Create a task
                </Link>
              </div>
            )}
          </div>
        ) : (
          <div className={`space-y-2 sm:space-y-3 ${loading && !initialLoad ? 'opacity-50' : ''}`}>
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
                    <div className="flex-1 min-w-0">
                      <h3 className="text-base sm:text-lg font-semibold text-gray-900 leading-tight">
                        {task.title}
                        <span className="text-xs text-gray-400 font-normal ml-2">#{task.id}</span>
                      </h3>
                    </div>
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
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span className="font-medium text-gray-700">
                        {task.owner_username || `User ${task.owner_user_id}`}
                      </span>
                    </div>
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

      {/* Pagination - Bottom */}
      <div className="my-4">
        <PaginationControls />
      </div>
    </div>
  );
}

export default TaskListPage;
