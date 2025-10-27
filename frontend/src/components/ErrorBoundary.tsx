import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
          <div className="max-w-md w-full">
            <div className="card text-center">
              <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
              
              <h1 className="text-2xl font-bold text-white mb-2">
                Coś poszło nie tak
              </h1>
              
              <p className="text-gray-400 mb-6">
                Aplikacja napotkała nieoczekiwany błąd. Spróbuj odświeżyć stronę lub wróć do strony głównej.
              </p>

              {process.env.NODE_ENV === 'development' && this.state.error && (
                <div className="mb-6 p-4 bg-red-900/20 border border-red-500/20 rounded-lg text-left">
                  <h3 className="text-sm font-semibold text-red-400 mb-2">Szczegóły błędu:</h3>
                  <pre className="text-xs text-red-300 whitespace-pre-wrap overflow-auto max-h-32">
                    {this.state.error.toString()}
                    {this.state.errorInfo?.componentStack}
                  </pre>
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-3">
                <button
                  onClick={this.handleReset}
                  className="btn btn-primary flex items-center justify-center space-x-2 flex-1"
                >
                  <RefreshCw className="w-4 h-4" />
                  <span>Spróbuj ponownie</span>
                </button>
                
                <button
                  onClick={() => window.location.href = '/'}
                  className="btn btn-secondary flex items-center justify-center space-x-2 flex-1"
                >
                  <Home className="w-4 h-4" />
                  <span>Strona główna</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
