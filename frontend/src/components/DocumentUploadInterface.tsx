import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, X, Loader, CheckCircle, AlertCircle } from 'lucide-react';

interface UploadedFile {
  file: File;
  status: 'pending' | 'uploaded' | 'error';
  error?: string;
}

interface DocumentUploadProps {
  projectId: number;
  onComplete: (resultId: number) => void;
}

export default function DocumentUploadInterface({ projectId, onComplete }: DocumentUploadProps) {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');

  const acceptedTypes = {
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'application/vnd.ms-excel': ['.xls'],
    'application/pdf': ['.pdf'],
    'text/plain': ['.txt'],
    'text/markdown': ['.md'],
    'text/csv': ['.csv']
  };

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    handleFiles(droppedFiles);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      handleFiles(selectedFiles);
    }
  };

  const handleFiles = (newFiles: File[]) => {
    const validFiles = newFiles.filter(file => {
      const ext = '.' + file.name.split('.').pop()?.toLowerCase();
      const validExts = ['.xlsx', '.xls', '.pdf', '.txt', '.md', '.csv'];
      return validExts.includes(ext);
    });

    if (validFiles.length !== newFiles.length) {
      setError('Niektóre pliki zostały pominięte (nieprawidłowy format)');
      setTimeout(() => setError(''), 3000);
    }

    const uploadedFiles: UploadedFile[] = validFiles.map(file => ({
      file,
      status: 'pending'
    }));

    setFiles(prev => [...prev, ...uploadedFiles]);
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setError('Dodaj przynajmniej jeden plik');
      return;
    }

    setIsProcessing(true);
    setProgress(0);
    setError('');

    const formData = new FormData();
    files.forEach(({ file }) => {
      formData.append('files', file);
    });

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 500);

      const response = await fetch(`http://localhost:8000/api/projects/${projectId}/documents/upload`, {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const result = await response.json();
      
      // Update file statuses
      setFiles(prev => prev.map(f => ({ ...f, status: 'uploaded' as const })));

      // Navigate to review page after short delay
      setTimeout(() => {
        onComplete(result.processing_result_id);
      }, 1000);

    } catch (err: any) {
      setError(err.message || 'Błąd podczas przetwarzania dokumentów');
      setFiles(prev => prev.map(f => ({ ...f, status: 'error' as const, error: err.message })));
    } finally {
      setIsProcessing(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    return <FileText className="w-8 h-8 text-primary-500" />;
  };

  return (
    <div className="space-y-6">
      <div className="bg-dark-800 p-6 rounded-lg">
        <h2 className="text-2xl font-bold text-white mb-2">
          Prześlij dokumenty do analizy
        </h2>
        <p className="text-gray-400 mb-6">
          Możesz przesłać pliki Excel, PDF, TXT, MD lub CSV zawierające informacje o firmie i procesach.
          Claude automatycznie wyciągnie dane i zmapuje je na formularz audytowy.
        </p>

        {/* Dropzone */}
        <div
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging
              ? 'border-primary-500 bg-primary-500/10'
              : 'border-dark-600 hover:border-dark-500'
          }`}
        >
          <Upload className={`w-16 h-16 mx-auto mb-4 ${isDragging ? 'text-primary-500' : 'text-gray-500'}`} />
          
          {isDragging ? (
            <p className="text-primary-500 text-lg font-semibold">Upuść pliki tutaj...</p>
          ) : (
            <>
              <p className="text-white text-lg mb-2">
                Przeciągnij i upuść pliki tutaj
              </p>
              <p className="text-gray-400 mb-4">lub</p>
              <label className="btn btn-primary cursor-pointer">
                <span>Wybierz pliki</span>
                <input
                  type="file"
                  multiple
                  onChange={handleFileInput}
                  accept=".xlsx,.xls,.pdf,.txt,.md,.csv"
                  className="hidden"
                />
              </label>
              <p className="text-sm text-gray-500 mt-4">
                Wspierane: Excel (.xlsx, .xls), PDF, TXT, Markdown (.md), CSV
              </p>
              <p className="text-xs text-gray-600 mt-2">
                Maksymalnie 10 plików, 50MB na plik, 200MB łącznie
              </p>
            </>
          )}
        </div>
      </div>

      {/* Files List */}
      {files.length > 0 && (
        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-4">
            Przesłane pliki ({files.length})
          </h3>
          
          <div className="space-y-3">
            {files.map((uploadedFile, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-dark-700 rounded-lg"
              >
                <div className="flex items-center space-x-3 flex-1">
                  {getFileIcon(uploadedFile.file.name)}
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate">
                      {uploadedFile.file.name}
                    </p>
                    <p className="text-sm text-gray-400">
                      {formatFileSize(uploadedFile.file.size)}
                    </p>
                    {uploadedFile.error && (
                      <p className="text-sm text-red-500 mt-1">{uploadedFile.error}</p>
                    )}
                  </div>
                  <div>
                    {uploadedFile.status === 'pending' && !isProcessing && (
                      <span className="text-gray-400">Oczekuje</span>
                    )}
                    {uploadedFile.status === 'pending' && isProcessing && (
                      <Loader className="w-5 h-5 text-primary-500 animate-spin" />
                    )}
                    {uploadedFile.status === 'uploaded' && (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    )}
                    {uploadedFile.status === 'error' && (
                      <AlertCircle className="w-5 h-5 text-red-500" />
                    )}
                  </div>
                </div>
                
                {!isProcessing && (
                  <button
                    onClick={() => removeFile(index)}
                    className="ml-4 p-2 text-gray-400 hover:text-red-500 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Progress */}
      {isProcessing && (
        <div className="bg-dark-800 p-6 rounded-lg">
          <div className="flex items-center space-x-3 mb-4">
            <Loader className="w-6 h-6 text-primary-500 animate-spin" />
            <h3 className="text-lg font-semibold text-white">
              Przetwarzanie dokumentów...
            </h3>
          </div>
          
          <div className="w-full bg-dark-700 rounded-full h-2 mb-4">
            <div
              className="bg-primary-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
          
          <div className="space-y-2 text-sm text-gray-400">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse"></div>
              <span>Parsowanie dokumentów...</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
              <span>Ekstrakcja danych przez Claude AI...</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
              <span>Mapowanie na strukturę BFA...</span>
            </div>
          </div>
          
          <p className="text-xs text-gray-500 mt-4">
            To może potrwać 2-5 minut w zależności od ilości danych...
          </p>
        </div>
      )}

      {/* Error */}
      {error && !isProcessing && (
        <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Actions */}
      {files.length > 0 && !isProcessing && (
        <div className="flex justify-between items-center">
          <button
            onClick={() => setFiles([])}
            className="btn btn-secondary"
          >
            Wyczyść wszystkie
          </button>
          <button
            onClick={handleUpload}
            className="btn btn-primary flex items-center space-x-2"
          >
            <Upload className="w-5 h-5" />
            <span>Przetwórz dokumenty ({files.length})</span>
          </button>
        </div>
      )}
    </div>
  );
}
