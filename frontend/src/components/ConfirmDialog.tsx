import { AlertTriangle, X } from 'lucide-react';

interface ConfirmDialogProps {
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
  variant?: 'danger' | 'warning' | 'info';
}

export default function ConfirmDialog({
  title,
  message,
  confirmLabel = 'Potwierdź',
  cancelLabel = 'Anuluj',
  onConfirm,
  onCancel,
  variant = 'warning',
}: ConfirmDialogProps) {
  const variantClasses = {
    danger: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500',
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
      <div className="card max-w-md w-full mx-4 animate-scale-in">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <AlertTriangle className={`w-6 h-6 ${variantClasses[variant]}`} />
            <h3 className="text-xl font-semibold text-white">{title}</h3>
          </div>
          <button
            onClick={onCancel}
            className="text-gray-500 hover:text-gray-300 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <p className="text-gray-300 mb-6">{message}</p>

        <div className="flex space-x-3">
          <button onClick={onCancel} className="btn btn-secondary flex-1">
            {cancelLabel}
          </button>
          <button
            onClick={onConfirm}
            className={`btn flex-1 ${
              variant === 'danger'
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'btn-primary'
            }`}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
