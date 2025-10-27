import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import { ToastType } from '../components/Toast';

interface Toast {
  id: string;
  type: ToastType;
  message: string;
  timestamp: number;
  duration?: number;
}

interface ToastState {
  toasts: Toast[];
  maxToasts: number;
  addToast: (type: ToastType, message: string, duration?: number) => void;
  removeToast: (id: string) => void;
  clearAllToasts: () => void;
  success: (message: string, duration?: number) => void;
  error: (message: string, duration?: number) => void;
  warning: (message: string, duration?: number) => void;
  info: (message: string, duration?: number) => void;
}

// Generate a more robust ID
const generateId = (): string => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

// Auto-remove toasts after duration
const autoRemoveToast = (id: string, duration: number, removeToast: (id: string) => void) => {
  setTimeout(() => {
    removeToast(id);
  }, duration);
};

export const useToastStore = create<ToastState>()(
  subscribeWithSelector((set, get) => ({
    toasts: [],
    maxToasts: 5, // Limit number of toasts

    addToast: (type, message, duration = 5000) => {
      const id = generateId();
      const toast: Toast = {
        id,
        type,
        message,
        timestamp: Date.now(),
        duration,
      };

      set((state) => {
        // Remove oldest toasts if we exceed maxToasts
        const newToasts = [...state.toasts, toast];
        if (newToasts.length > state.maxToasts) {
          newToasts.splice(0, newToasts.length - state.maxToasts);
        }
        return { toasts: newToasts };
      });

      // Auto-remove after duration
      if (duration > 0) {
        autoRemoveToast(id, duration, get().removeToast);
      }
    },

    removeToast: (id) => {
      set((state) => ({
        toasts: state.toasts.filter((toast) => toast.id !== id),
      }));
    },

    clearAllToasts: () => {
      set({ toasts: [] });
    },

    success: (message, duration = 5000) => {
      get().addToast('success', message, duration);
    },

    error: (message, duration = 7000) => {
      get().addToast('error', message, duration);
    },

    warning: (message, duration = 6000) => {
      get().addToast('warning', message, duration);
    },

    info: (message, duration = 4000) => {
      get().addToast('info', message, duration);
    },
  }))
);
