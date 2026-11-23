import type {
  CurriculumResponse,
  HintResponse,
  LessonDetail,
  LessonProgress,
  ModuleGroup,
  OracleResponse,
  PortfolioProject,
  ProgressBackupPayload,
  ProjectsResponse,
  RunResponse,
} from '../types/api';

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });
  const contentType = res.headers.get('content-type') ?? '';
  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    if (contentType.includes('application/json')) {
      try {
        const errBody = await res.json();
        if (errBody?.detail) {
          message = String(errBody.detail);
        } else if (errBody?.error) {
          message = String(errBody.error);
        }
      } catch {
        // ignore parse errors
      }
    }
    throw new Error(message);
  }
  if (!contentType.includes('application/json')) {
    throw new Error('Server returned a non-JSON response. Ensure the PyQuest backend is running.');
  }
  return res.json() as Promise<T>;
}

export const api = {
  getCurriculum(): Promise<CurriculumResponse> {
    return requestJson<CurriculumResponse>('/api/curriculum');
  },

  getModule(id: string): Promise<ModuleGroup> {
    return requestJson<ModuleGroup>(`/api/modules/${encodeURIComponent(id)}`);
  },

  getLesson(id: string): Promise<LessonDetail> {
    return requestJson<LessonDetail>(`/api/lessons/${encodeURIComponent(id)}`);
  },

  saveDraft(
    id: string,
    files: Record<string, string>
  ): Promise<{ lessonId: string; files: Record<string, string> }> {
    return requestJson(`/api/lessons/${encodeURIComponent(id)}/draft`, {
      method: 'POST',
      body: JSON.stringify({ files }),
    });
  },

  runTests(id: string, files: Record<string, string>): Promise<RunResponse> {
    return requestJson<RunResponse>(`/api/lessons/${encodeURIComponent(id)}/run`, {
      method: 'POST',
      body: JSON.stringify({ files }),
    });
  },

  revealHint(id: string): Promise<HintResponse> {
    return requestJson<HintResponse>(`/api/lessons/${encodeURIComponent(id)}/hint`, {
      method: 'POST',
      body: JSON.stringify({}),
    });
  },

  saveNotes(id: string, notes: string): Promise<LessonProgress> {
    return requestJson<LessonProgress>(`/api/lessons/${encodeURIComponent(id)}/notes`, {
      method: 'POST',
      body: JSON.stringify({ notes }),
    });
  },

  toggleFlag(id: string, flagged: boolean): Promise<LessonProgress> {
    return requestJson<LessonProgress>(`/api/lessons/${encodeURIComponent(id)}/flag`, {
      method: 'POST',
      body: JSON.stringify({ flagged }),
    });
  },

  askOracle(
    lessonId: string,
    question: string,
    files: Record<string, string>,
    lastDiagnostics = ''
  ): Promise<OracleResponse> {
    return requestJson<OracleResponse>('/api/oracle/ask', {
      method: 'POST',
      body: JSON.stringify({ lessonId, question, files, lastDiagnostics }),
    });
  },

  resetLesson(id: string): Promise<{ lessonId: string; files: Record<string, string> }> {
    return requestJson(`/api/lessons/${encodeURIComponent(id)}/reset`, {
      method: 'POST',
      body: JSON.stringify({}),
    });
  },

  getSolution(id: string): Promise<{ lessonId: string; files: Record<string, string> }> {
    return requestJson(`/api/lessons/${encodeURIComponent(id)}/solution`);
  },

  getProjects(): Promise<ProjectsResponse> {
    return requestJson<ProjectsResponse>('/api/projects');
  },

  updateProjectChecklist(
    projectId: string,
    itemId: string,
    checked: boolean
  ): Promise<PortfolioProject> {
    return requestJson<PortfolioProject>(
      `/api/projects/${encodeURIComponent(projectId)}/checklist`,
      {
        method: 'POST',
        body: JSON.stringify({ itemId, checked }),
      }
    );
  },

  updateProjectRepo(
    projectId: string,
    repoUrl: string,
    completed?: boolean
  ): Promise<PortfolioProject> {
    return requestJson<PortfolioProject>(`/api/projects/${encodeURIComponent(projectId)}/repo`, {
      method: 'POST',
      body: JSON.stringify({ repoUrl, ...(completed !== undefined ? { completed } : {}) }),
    });
  },

  exportProgress(): Promise<ProgressBackupPayload> {
    return requestJson<ProgressBackupPayload>('/api/progress/export');
  },

  importProgress(payload: ProgressBackupPayload): Promise<{ status: string }> {
    return requestJson<{ status: string }>('/api/progress/import', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  resetAllProgress(): Promise<{ status: string }> {
    return requestJson<{ status: string }>('/api/progress/reset', {
      method: 'POST',
      body: JSON.stringify({}),
    });
  },
};
