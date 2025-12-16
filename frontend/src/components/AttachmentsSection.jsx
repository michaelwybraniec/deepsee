import { useState, useEffect, useRef } from 'react';
import { toast } from 'sonner';
import { uploadAttachment, listAttachments, deleteAttachment } from '../services/attachmentApi';
import { useAuth } from '../contexts/AuthContext';

function AttachmentsSection({ taskId, isOwner }) {
  const { user } = useAuth();
  const [attachments, setAttachments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchAttachments();
  }, [taskId]);

  const fetchAttachments = async () => {
    setLoading(true);
    setError('');
    const result = await listAttachments(taskId);
    
    if (result.success) {
      setAttachments(result.data || []);
    } else {
      setError(result.error || 'Failed to load attachments');
    }
    setLoading(false);
  };

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Client-side validation
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setError('File size must be less than 10MB');
      return;
    }

    setUploading(true);
    setError('');

    const result = await uploadAttachment(taskId, file);

    if (result.success) {
      // Refresh attachment list
      await fetchAttachments();
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } else {
      setError(result.error || 'Failed to upload attachment');
    }

    setUploading(false);
  };

  const handleDelete = async (attachmentId) => {
    if (!window.confirm('Are you sure you want to delete this attachment?')) {
      return;
    }

    const result = await deleteAttachment(attachmentId);

    if (result.success) {
      // Remove attachment from list (optimistic update)
      setAttachments((prev) => prev.filter((att) => att.id !== attachmentId));
    } else {
      setError(result.error || 'Failed to delete attachment');
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return 'Unknown size';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Attachments</h2>
          {isOwner && (
            <div>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                disabled={uploading}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {uploading ? 'Uploading...' : 'Upload File'}
              </label>
            </div>
          )}
        </div>

        {error && (
          <div className="mt-4 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}

        {loading ? (
          <div className="mt-4 text-sm text-gray-600">Loading attachments...</div>
        ) : attachments.length === 0 ? (
          <div className="mt-4 text-sm text-gray-500">No attachments</div>
        ) : (
          <ul className="mt-4 divide-y divide-gray-200">
            {attachments.map((attachment) => (
              <li key={attachment.id} className="py-3 flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {attachment.file_name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {formatFileSize(attachment.file_size)} • Uploaded {formatDate(attachment.uploaded_at)}
                  </p>
                </div>
                {isOwner && (
                  <button
                    onClick={() => handleDelete(attachment.id)}
                    className="ml-4 px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    Delete
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default AttachmentsSection;
