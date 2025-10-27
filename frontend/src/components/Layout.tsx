import { useNavigate } from 'react-router-dom';
import { Home } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-dark-800">
      <nav className="bg-dark-900 border-b border-dark-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="flex items-center space-x-2 text-primary-500 hover:text-primary-400"
              >
                <Home className="w-6 h-6" />
                <span className="font-bold text-xl">BFA Audit App</span>
              </button>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-400 text-sm">Aplikacja wewnętrzna - Audyty Automatyzacyjne</span>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
