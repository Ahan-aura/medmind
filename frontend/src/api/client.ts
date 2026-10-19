const BASE_URL = '/api';

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetail = response.statusText;
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errorDetail;
    } catch {
      // ignore
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const api = {
  auth: {
    login: (credentials: { email: string; password: string }) =>
      apiRequest<{ access_token: string; user: any }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      }),
    register: (data: any) =>
      apiRequest<{ access_token: string; user: any }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    me: () => apiRequest<any>('/auth/me'),
  },
  cases: {
    list: () => apiRequest<any[]>('/cases'),
    get: (id: string) => apiRequest<any>(`/cases/${id}`),
  },
  attempts: {
    start: (caseId: string, lang = 'en', parentAttemptId?: string | null) =>
      apiRequest<any>('/attempts', {
        method: 'POST',
        body: JSON.stringify({
          case_id: caseId,
          lang,
          parent_attempt_id: parentAttemptId || null,
        }),
      }),
    get: (attemptId: string) => apiRequest<any>(`/attempts/${attemptId}`),
    step: (attemptId: string, nodeId: string, choiceId: string) =>
      apiRequest<any>(`/attempts/${attemptId}/step`, {
        method: 'POST',
        body: JSON.stringify({ node_id: nodeId, choice_id: choiceId }),
      }),
    submit: (attemptId: string, data: {
      selected_answer: string;
      reasoning_text: string;
      selected_evidence: string[];
      confidence: number;
    }) =>
      apiRequest<any>(`/attempts/${attemptId}/submit`, {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    feedback: (attemptId: string) =>
      apiRequest<any>(`/attempts/${attemptId}/feedback`, {
        method: 'POST',
      }),
    lessonComplete: (attemptId: string, answers: Record<string, string> = {}) =>
      apiRequest<any>(`/attempts/${attemptId}/lesson-complete`, {
        method: 'POST',
        body: JSON.stringify({ answers }),
      }),
    reassess: (attemptId: string) =>
      apiRequest<any>(`/attempts/${attemptId}/reassess`, {
        method: 'POST',
      }),
  },
  lessons: {
    get: (lessonId: string) => apiRequest<any>(`/lessons/${lessonId}`),
  },
  progress: {
    getMe: () => apiRequest<any>('/progress/me'),
  },
  teacher: {
    getSummary: (cohortId: string) => apiRequest<any>(`/teacher/cohorts/${cohortId}/summary`),
  },
};
