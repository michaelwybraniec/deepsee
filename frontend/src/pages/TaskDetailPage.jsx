import { useParams } from 'react-router-dom';

function TaskDetailPage() {
  const { id } = useParams();

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Task Detail</h1>
      <p className="text-gray-600 mb-4">
        Task ID: <span className="font-mono">{id}</span>
      </p>
      <p className="text-gray-600">
        Task detail view will be implemented in task 10.4
      </p>
    </div>
  );
}

export default TaskDetailPage;
