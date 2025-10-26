import axios from 'axios';
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

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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

export default api;
