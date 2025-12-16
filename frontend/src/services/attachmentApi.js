import apiClient from './api';

/**
 * Attachment API client
 * Handles all attachment-related API calls
 */

export const uploadAttachment = async (taskId, file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post(`/api/tasks/${taskId}/attachments`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to upload attachment';
    return { success: false, error: errorMessage };
  }
};

export const listAttachments = async (taskId) => {
  try {
    const response = await apiClient.get(`/api/tasks/${taskId}/attachments`);
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to fetch attachments';
    return { success: false, error: errorMessage };
  }
};

export const deleteAttachment = async (attachmentId) => {
  try {
    await apiClient.delete(`/api/attachments/${attachmentId}`);
    return { success: true };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to delete attachment';
    return { success: false, error: errorMessage };
  }
};
