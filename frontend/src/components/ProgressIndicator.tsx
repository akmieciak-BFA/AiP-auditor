import { Save, Check } from 'lucide-react';
import { useEffect, useState } from 'react';

interface ProgressIndicatorProps {
  isSaving?: boolean;
  lastSaved?: Date | null;
  progress?: number; // 0-100
  label?: string;
}

export default function ProgressIndicator({
  isSaving = false,
  lastSaved = null,
  progress,
  label = 'Postęp',
}: ProgressIndicatorProps) {
  const [showSaved, setShowSaved] = useState(false);

  useEffect(() => {
    if (lastSaved) {
      setShowSaved(true);
      const timer = setTimeout(() => setShowSaved(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [lastSaved]);

  const formatLastSaved = (date: Date) => {
    const now = new Date();
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diff < 60) return 'przed chwilą';
    if (diff < 3600) return `${Math.floor(diff / 60)} min temu`;
    return date.toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex items-center space-x-4">
      {/* Progress Bar */}
      {progress !== undefined && (
        <div className="flex-1">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm text-gray-400">{label}</span>
            <span className="text-sm font-semibold text-primary-500">{progress}%</span>
          </div>
          <div className="h-2 bg-dark-600 rounded-full overflow-hidden">
            <div
              className="h-full bg-primary-500 transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Auto-save Indicator */}
      <div className="flex items-center space-x-2 text-sm">
        {isSaving ? (
          <>
            <Save className="w-4 h-4 text-gray-400 animate-pulse" />
            <span className="text-gray-400">Zapisywanie...</span>
          </>
        ) : showSaved && lastSaved ? (
          <>
            <Check className="w-4 h-4 text-green-500" />
            <span className="text-green-500">Zapisano {formatLastSaved(lastSaved)}</span>
          </>
        ) : lastSaved ? (
          <span className="text-gray-500 text-xs">
            Zapisano {formatLastSaved(lastSaved)}
          </span>
        ) : null}
      </div>
    </div>
  );
}
