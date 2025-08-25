const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Debug logging to verify environment variable is loaded
console.log("API_URL configured as:", API_URL);
console.log("NEXT_PUBLIC_API_URL from env:", process.env.NEXT_PUBLIC_API_URL);

const refreshToken = async () => {
  console.log("Attempting to refresh token...");
  try {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
      throw new Error("No refresh token found");
    }
    const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshToken}`
      },
    });
    if (!response.ok) {
      console.error("Failed to refresh token, status:", response.status);
      throw new Error('Failed to refresh token');
    }
    const data = await response.json();
    localStorage.setItem('accessToken', data.access_token);
    console.log("Token refreshed successfully.");
  } catch (error) {
    console.error("Error refreshing token:", error);
    // It's better to redirect to login if refresh fails
    // window.location.href = '/login';
    throw error;
  }
};

const api = {
  get: async (path: string) => {
    console.log(`GET request to: ${path}`);
    let response = await fetch(`${API_URL}/api/v1${path}`, {
      headers: getAuthHeaders(),
    });
    console.log(`Initial response status: ${response.status}`);
    if (response.status === 401) {
      console.log("Token expired, attempting to refresh...");
      await refreshToken();
      console.log("Retrying GET request...");
      response = await fetch(`${API_URL}/api/v1${path}`, {
        headers: getAuthHeaders(),
      });
      console.log(`Retry response status: ${response.status}`);
    }
    if (!response.ok) {
      console.error(`Failed to fetch ${path}, status: ${response.status}`);
      throw new Error(`Failed to fetch ${path}`);
    }
    return response.json();
  },
  post: async (path: string, data: any) => {
    let response = await fetch(`${API_URL}/api/v1${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(data),
    });
    if (response.status === 401) {
      await refreshToken();
      response = await fetch(`${API_URL}/api/v1${path}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify(data),
      });
    }
    if (!response.ok) {
      throw new Error(`Failed to post to ${path}`);
    }
    return response.json();
  },
  put: async (path: string, data: any) => {
    let response = await fetch(`${API_URL}/api/v1${path}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(data),
    });
    if (response.status === 401) {
      await refreshToken();
      response = await fetch(`${API_URL}/api/v1${path}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify(data),
      });
    }
    if (!response.ok) {
      throw new Error(`Failed to put to ${path}`);
    }
    return response.json();
  },
  delete: async (path: string) => {
    let response = await fetch(`${API_URL}/api/v1${path}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    if (response.status === 401) {
      await refreshToken();
      response = await fetch(`${API_URL}/api/v1${path}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });
    }
    if (!response.ok) {
      throw new Error(`Failed to delete ${path}`);
    }
    // For DELETE, we might not always have a JSON response
    // return response.json();
  },
};

export { api };
const getAuthHeaders = (): HeadersInit => {
    const token = localStorage.getItem('accessToken');
    const headers: HeadersInit = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
};

export interface Note {
  id: string;
  client_name: string;
  meeting_date: string;
  content: string;
}

export async function getNotes(): Promise<Note[]> {
  const response = await fetch(`${API_URL}/api/v1/notes`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error("Failed to fetch notes");
  }
  return response.json();
}

export async function getNoteById(id: number): Promise<Note> {
  const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error("Failed to fetch note");
  }
  return response.json();
}

export async function createNote(note: Omit<Note, "id">): Promise<Note> {
  const response = await fetch(`${API_URL}/api/v1/notes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(note),
  });
  if (!response.ok) {
    throw new Error("Failed to create note");
  }
  return response.json();
}

export async function updateNote(
  id: number,
  note: Partial<Omit<Note, "id">>
): Promise<Note> {
  const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(note),
  });
  if (!response.ok) {
    throw new Error("Failed to update note");
  }
  return response.json();
}

export async function deleteNote(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/api/v1/notes/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error("Failed to delete note");
  }
}
export interface Client {
  id: string;
  name: string;
  description: string;
  meetingNotes?: string;
}

export async function getClients(): Promise<Client[]> {
  const response = await fetch(`${API_URL}/api/v1/clients/`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error("Failed to fetch clients");
  }
  const data = await response.json();
  return data.map((client: any) => ({
    ...client,
    id: client._id,
  }));
}

export async function getClientById(id: string): Promise<Client> {
  const response = await fetch(`${API_URL}/api/v1/clients/${id}`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    throw new Error("Failed to fetch client");
  }
  const data = await response.json();
  return {
    ...data,
    id: data._id,
  };
}

export async function createClient(
  client: Omit<Client, "id">
): Promise<Client> {
  return api.post("/clients/", client);
}

export async function getUpcomingMeetings(): Promise<any[]> {
  return api.get("/integrations/google/upcoming-meetings");
}

export async function getGoogleAuthorizationUrl(): Promise<{
  authorization_url: string;
}> {
  const response = await fetch(
    `${API_URL}/api/v1/integrations/google/authorization-url`,
    {
      headers: getAuthHeaders(),
    }
  );
  if (!response.ok) {
    throw new Error("Failed to get Google authorization URL");
  }
  return response.json();
}

export async function getGoogleCalendarConnectionStatus(): Promise<{
  is_connected: boolean;
  connected_at?: string;
  email?: string;
}> {
  const response = await fetch(
    `${API_URL}/api/v1/integrations/google/connection-status`,
    {
      headers: getAuthHeaders(),
    }
  );
  if (!response.ok) {
    throw new Error("Failed to get Google Calendar connection status");
  }
  return response.json();
}

export async function handleGoogleCallback(
  code: string,
  state: string
): Promise<any> {
  const response = await fetch(
    `${API_URL}/api/v1/integrations/google/callback?code=${code}&state=${state}`,
    {
      headers: getAuthHeaders(),
    }
  );
  if (!response.ok) {
    throw new Error("Failed to handle Google callback");
  }
  return response.json();
}

export async function updateClient(
  id: string,
  client: Partial<Omit<Client, "id">>
): Promise<Client> {
  const response = await fetch(`${API_URL}/api/v1/clients/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(client),
  });
  if (!response.ok) {
    throw new Error("Failed to update client");
  }
  return response.json();
}

export async function deleteClient(id: string): Promise<void> {
  return api.delete(`/clients/${id}`);
}
