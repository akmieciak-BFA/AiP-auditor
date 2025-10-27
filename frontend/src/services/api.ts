import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import type {
  Project,
  ProjectCreate,
  Step1Input,
  Step1Result,
  Step2ProcessData,
  Step2Result,
  Step3Input,
  Step4GenerateRequest,
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with optimized configuration
const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
  // Enable request/response compression
  decompress: true,
});

// Request interceptor for logging and error handling
api.interceptors.request.use(
  (config) => {
    // Add timestamp to prevent caching issues
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now(),
      };
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    if (error.response?.status === 429) {
      // Rate limit exceeded
      const retryAfter = error.response.headers['retry-after'];
      console.warn(`Rate limit exceeded. Retry after ${retryAfter} seconds`);
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
    } else if (!error.response) {
      console.error('Network error - please check your connection');
    }
    return Promise.reject(error);
  }
);

// Helper function to download file
const downloadFile = (data: Blob, filename: string) => {
  const url = window.URL.createObjectURL(data);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

// Projects
export const projectsAPI = {
  getAll: async (): Promise<Project[]> => {
    const response = await api.get('/api/projects');
    return response.data;
  },

  getOne: async (id: number): Promise<Project> => {
    const response = await api.get(`/api/projects/${id}`);
    return response.data;
  },

  create: async (data: ProjectCreate): Promise<Project> => {
    const response = await api.post('/api/projects', data);
    return response.data;
  },

  update: async (id: number, data: Partial<ProjectCreate>): Promise<Project> => {
    const response = await api.put(`/api/projects/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/projects/${id}`);
  },
};

// Step 1
export const step1API = {
  generateForm: async (projectId: number, orgData: any) => {
    const response = await api.post(`/api/projects/${projectId}/step1/generate-form`, orgData);
    return response.data;
  },

  analyze: async (projectId: number, data: Step1Input): Promise<Step1Result> => {
    const response = await api.post(`/api/projects/${projectId}/step1/analyze`, data);
    return response.data;
  },

  getResults: async (projectId: number): Promise<Step1Result> => {
    const response = await api.get(`/api/projects/${projectId}/step1/results`);
    return response.data;
  },
};

// Step 2
export const step2API = {
  addProcess: async (projectId: number, processName: string) => {
    const response = await api.post(
      `/api/projects/${projectId}/step2/processes?process_name=${encodeURIComponent(processName)}`
    );
    return response.data;
  },

  updateProcess: async (
    projectId: number,
    processId: number,
    data: Step2ProcessData
  ) => {
    const response = await api.put(
      `/api/projects/${projectId}/step2/processes/${processId}`,
      data
    );
    return response.data;
  },

  analyzeProcess: async (
    projectId: number,
    processId: number
  ): Promise<Step2Result> => {
    const response = await api.post(
      `/api/projects/${projectId}/step2/processes/${processId}/analyze`
    );
    return response.data;
  },

  getResults: async (projectId: number) => {
    const response = await api.get(`/api/projects/${projectId}/step2/results`);
    return response.data;
  },
};

// Step 3
export const step3API = {
  analyze: async (projectId: number, data: Step3Input) => {
    const response = await api.post(`/api/projects/${projectId}/step3/analyze`, data);
    return response.data;
  },

  getResults: async (projectId: number) => {
    const response = await api.get(`/api/projects/${projectId}/step3/results`);
    return response.data;
  },
};

// Step 4
export const step4API = {
  generatePresentation: async (projectId: number, data: Step4GenerateRequest) => {
    const response = await api.post(
      `/api/projects/${projectId}/step4/generate-presentation`,
      data
    );
    return response.data;
  },

  getDownloads: async (projectId: number) => {
    const response = await api.get(`/api/projects/${projectId}/step4/downloads`);
    return response.data;
  },
};

// Downloads
export const downloadsAPI = {
  downloadMarkdown: async (projectId: number, projectName: string, clientName: string) => {
    const response = await api.get(`/api/projects/${projectId}/download/markdown`, {
      responseType: 'blob',
    });
    
    // Generate filename
    const safeProjectName = projectName.replace(/\s+/g, '_').replace(/[/\\]/g, '_');
    const safeClientName = clientName.replace(/\s+/g, '_').replace(/[/\\]/g, '_');
    const filename = `Audyt_BFA_${safeClientName}_${safeProjectName}.md`;
    
    downloadFile(response.data, filename);
  },

  previewMarkdown: async (projectId: number) => {
    const response = await api.get(`/api/projects/${projectId}/download/preview`);
    return response.data;
  },
};

export default api;
