const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('accessToken');
  const headers: HeadersInit = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export interface Note {
  id: number;
  title: string;
  content: string;
  createdAt: string;
}

export async function getNotes(): Promise<Note[]> {
  const response = await fetch(`${API_URL}/api/v1/notes`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error('Failed to fetch notes');
  }
  return response.json();
}

export async function getNoteById(id: number): Promise<Note> {
  const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error('Failed to fetch note');
  }
  return response.json();
}

export async function createNote(note: Omit<Note, 'id'>): Promise<Note> {
  const response = await fetch(`${API_URL}/api/v1/notes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(note),
  });
  if (!response.ok) {
    throw new Error('Failed to create note');
  }
  return response.json();
}

export async function updateNote(id: number, note: Partial<Omit<Note, 'id'>>): Promise<Note> {
  const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(note),
  });
  if (!response.ok) {
    throw new Error('Failed to update note');
  }
  return response.json();
}

export async function deleteNote(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error('Failed to delete note');
  }
}
export interface Group {
  id: number;
  name: string;
  description: string;
}

export async function getGroups(): Promise<Group[]> {
  const response = await fetch(`${API_URL}/api/v1/groups/`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error('Failed to fetch groups');
  }
  return response.json();
}

export async function createGroup(group: Omit<Group, 'id'>): Promise<Group> {
  const response = await fetch(`${API_URL}/api/v1/groups/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(group),
  });
  if (!response.ok) {
    throw new Error('Failed to create group');
  }
  return response.json();
}

export async function updateGroup(id: number, group: Partial<Omit<Group, 'id'>>): Promise<Group> {
  const response = await fetch(`${API_URL}/api/v1/groups/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(group),
  });
  if (!response.ok) {
    throw new Error('Failed to update group');
  }
  return response.json();
}

export async function deleteGroup(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/api/v1/groups/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error('Failed to delete group');
  }
}