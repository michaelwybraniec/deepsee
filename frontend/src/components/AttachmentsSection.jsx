import { useState, useEffect, useRef, useCallback } from 'react';
import { toast } from 'sonner';
import { uploadAttachment, listAttachments, deleteAttachment } from '../services/attachmentApi';

function AttachmentsSection({ taskId, isOwner }) {
  const [attachments, setAttachments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const fetchAttachments = useCallback(async () => {
    setLoading(true);
    setError('');
    const result = await listAttachments(taskId);
    
    if (result.success) {
      setAttachments(result.data || []);
    } else {
      setError(result.error || 'Failed to load attachments');
    }
    setLoading(false);
  }, [taskId]);

  useEffect(() => {
    fetchAttachments();
  }, [fetchAttachments]);

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
      toast.success('Attachment uploaded successfully!');
      // Refresh attachment list
      await fetchAttachments();
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } else {
      const errorMsg = result.error || 'Failed to upload attachment';
      setError(errorMsg);
      toast.error(errorMsg);
    }

    setUploading(false);
  };

  const handleDelete = async (attachmentId) => {
    if (!window.confirm('Are you sure you want to delete this attachment?')) {
      return;
    }

    const result = await deleteAttachment(attachmentId);

    if (result.success) {
      toast.success('Attachment deleted successfully!');
      // Remove attachment from list (optimistic update)
      setAttachments((prev) => prev.filter((att) => att.id !== attachmentId));
    } else {
      const errorMsg = result.error || 'Failed to delete attachment';
      setError(errorMsg);
      toast.error(errorMsg);
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
    <div>
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-4">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Attachments</h2>
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
              className={`inline-flex items-center px-4 py-2 bg-primary-500 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed transition-colors ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
              style={{ backgroundColor: '#3b82f6' }}
            >
              {uploading ? 'Uploading...' : 'Upload File'}
            </label>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
          <div className="text-sm text-red-800 font-medium">{error}</div>
        </div>
      )}

      {loading ? (
        <div className="text-sm text-gray-600">Loading attachments...</div>
      ) : attachments.length === 0 ? (
        <div className="text-sm text-gray-500">No attachments</div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {attachments.map((attachment) => (
            <li key={attachment.id} className="py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {attachment.file_name}
                </p>
                <p className="text-xs text-gray-500">
                  {formatFileSize(attachment.file_size)} • Uploaded {formatDate(attachment.uploaded_at)}
                </p>
              </div>
              {isOwner && (
                <button
                  onClick={() => handleDelete(attachment.id)}
                  className="px-3 py-1.5 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
                >
                  Delete
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default AttachmentsSection;
