import apiClient from './api';

/**
 * Task API client
 * Handles all task-related API calls
 */

export const getTasks = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/tasks/', { params });
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to fetch tasks';
    return { success: false, error: errorMessage };
  }
};

export const getTask = async (id) => {
  try {
    const response = await apiClient.get(`/api/tasks/${id}`);
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to fetch task';
    return { success: false, error: errorMessage };
  }
};

export const createTask = async (taskData) => {
  try {
    const response = await apiClient.post('/api/tasks/', taskData);
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to create task';
    return { success: false, error: errorMessage };
  }
};

export const updateTask = async (id, taskData) => {
  try {
    const response = await apiClient.put(`/api/tasks/${id}`, taskData);
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to update task';
    return { success: false, error: errorMessage };
  }
};

export const deleteTask = async (id) => {
  try {
    await apiClient.delete(`/api/tasks/${id}`);
    return { success: true };
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to delete task';
    return { success: false, error: errorMessage };
  }
};
