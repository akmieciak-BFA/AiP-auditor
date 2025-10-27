import { useEffect, useRef, useCallback } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface UseAutoSaveOptions {
  projectId: number;
  step: string;
  data: any;
  enabled?: boolean;
  interval?: number; // milliseconds
}

export function useAutoSave({
  projectId,
  step,
  data,
  enabled = true,
  interval = 30000, // 30 seconds default
}: UseAutoSaveOptions) {
  const timeoutRef = useRef<NodeJS.Timeout>();
  const lastSavedRef = useRef<string>('');

  const saveDraft = useCallback(async () => {
    if (!enabled || !data) return;

    const dataString = JSON.stringify(data);
    
    // Only save if data changed
    if (dataString === lastSavedRef.current) return;

    try {
      await axios.post(
        `${API_URL}/api/projects/${projectId}/drafts/save`,
        {
          step,
          draft_data: data,
        }
      );
      lastSavedRef.current = dataString;
      // Draft saved successfully (removed console.log for production)
    } catch (error) {
      console.error('Auto-save failed:', error);
    }
  }, [projectId, step, data, enabled]);

  useEffect(() => {
    if (!enabled) return;

    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set new timeout
    timeoutRef.current = setTimeout(saveDraft, interval);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [data, enabled, interval, saveDraft]);

  return { saveDraft };
}

export async function loadDraft(projectId: number, step: string) {
  try {
    const response = await axios.get(
      `${API_URL}/api/projects/${projectId}/drafts/load?step=${step}`
    );
    return response.data;
  } catch (error) {
    console.error('Load draft failed:', error);
    return { has_draft: false, draft_data: null };
  }
}

export async function clearDraft(projectId: number, step: string) {
  try {
    await axios.delete(
      `${API_URL}/api/projects/${projectId}/drafts/clear?step=${step}`
    );
  } catch (error) {
    console.error('Clear draft failed:', error);
  }
}
