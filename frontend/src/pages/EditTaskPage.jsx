import { useParams } from 'react-router-dom';

function EditTaskPage() {
  const { id } = useParams();

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Edit Task</h1>
      <p className="text-gray-600 mb-4">
        Task ID: <span className="font-mono">{id}</span>
      </p>
      <p className="text-gray-600">
        Edit task form will be implemented in task 10.4
      </p>
    </div>
  );
}

export default EditTaskPage;
