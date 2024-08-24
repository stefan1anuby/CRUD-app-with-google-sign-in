import axios from 'axios';
import { BACKEND_URL } from '../config';

export const fetchUserData = async () => {
  const token = localStorage.getItem('access_token');
  return axios.get(`${BACKEND_URL}/users/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const updateUserName = async (newName) => {
  const token = localStorage.getItem('access_token');
  return axios.put(`${BACKEND_URL}/users/me/name`, null, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    params: {
      new_name: newName,
    },
  });
};

export const addNote = async (noteContent) => {
  const token = localStorage.getItem('access_token');
  return axios.post(`${BACKEND_URL}/users/me/notes`, { content: noteContent }, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
};

export const deleteNote = async (noteId) => {
  const token = localStorage.getItem('access_token');
  return axios.delete(`${BACKEND_URL}/users/me/notes/${noteId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};
