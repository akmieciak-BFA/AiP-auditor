import React, { useState } from 'react';
import { downloadsAPI } from '../services/api';
import { useToastStore } from '../store/toastStore';

interface DownloadButtonProps {
  projectId: number;
  projectName: string;
  clientName: string;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export const DownloadButton: React.FC<DownloadButtonProps> = ({
  projectId,
  projectName,
  clientName,
  variant = 'primary',
  size = 'md',
}) => {
  const [isDownloading, setIsDownloading] = useState(false);
  const addToast = useToastStore((state) => state.addToast);

  const handleDownload = async () => {
    setIsDownloading(true);
    try {
      await downloadsAPI.downloadMarkdown(projectId, projectName, clientName);
      addToast({
        type: 'success',
        message: 'Raport Markdown został pobrany',
      });
    } catch (error: any) {
      console.error('Download failed:', error);
      addToast({
        type: 'error',
        message: error.response?.data?.message || 'Błąd pobierania raportu',
      });
    } finally {
      setIsDownloading(false);
    }
  };

  // Variant styles
  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50',
  };

  // Size styles
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      onClick={handleDownload}
      disabled={isDownloading}
      className={`
        flex items-center gap-2 rounded-lg font-medium transition-colors
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variantClasses[variant]}
        ${sizeClasses[size]}
      `}
    >
      {isDownloading ? (
        <>
          <svg
            className="animate-spin h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <span>Pobieranie...</span>
        </>
      ) : (
        <>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <span>Pobierz Markdown</span>
        </>
      )}
    </button>
  );
};
