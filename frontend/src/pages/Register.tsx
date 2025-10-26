import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useToastStore } from '../store/toastStore';
import { UserPlus } from 'lucide-react';

export default function Register() {
  const navigate = useNavigate();
  const { register: registerUser, isLoading } = useAuthStore();
  const toast = useToastStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Client-side validation
    if (!name || !email || !password) {
      setError('Wypełnij wszystkie pola');
      return;
    }
    
    if (name.length < 2) {
      setError('Imię i nazwisko musi mieć minimum 2 znaki');
      return;
    }
    
    if (password.length < 6) {
      setError('Hasło musi mieć minimum 6 znaków');
      return;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Nieprawidłowy format email');
      return;
    }
    
    try {
      await registerUser(email, password, name);
      toast.success('Konto utworzone pomyślnie!');
      navigate('/');
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || err.response?.data?.detail || 'Błąd rejestracji';
      setError(errorMsg);
      toast.error(errorMsg);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-dark-800 px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-primary-500 mb-2">BFA Audit App</h1>
          <p className="text-gray-400">Stwórz nowe konto</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Imię i nazwisko</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="input"
                placeholder="Jan Kowalski"
                required
              />
            </div>

            <div>
              <label className="label">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="twoj@email.com"
                required
              />
            </div>

            <div>
              <label className="label">Hasło</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="••••••••"
                required
                minLength={6}
              />
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-2 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="btn btn-primary w-full flex items-center justify-center space-x-2"
            >
              <UserPlus className="w-5 h-5" />
              <span>{isLoading ? 'Rejestracja...' : 'Zarejestruj się'}</span>
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Masz już konto?{' '}
              <Link to="/login" className="text-primary-500 hover:text-primary-400">
                Zaloguj się
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
