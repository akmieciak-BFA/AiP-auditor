import { useState } from 'react';
import { Loader, TrendingUp, DollarSign } from 'lucide-react';
import { step3API } from '../services/api';

interface Step3FormProps {
  projectId: number;
  onComplete: () => void;
}

export default function Step3Form({ projectId, onComplete }: Step3FormProps) {
  const [budgetLevel, setBudgetLevel] = useState<'low' | 'medium' | 'high'>('medium');
  const [results, setResults] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const analysisResults = await step3API.analyze(projectId, {
        budget_level: budgetLevel,
        tech_preferences: {},
      });
      setResults(analysisResults);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd analizy');
    } finally {
      setIsLoading(false);
    }
  };

  const handleComplete = () => {
    onComplete();
  };

  if (results) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white mb-4">Wyniki Rekomendacji Technologicznych</h2>

        <div className="bg-primary-500/10 border border-primary-500 text-primary-500 px-4 py-2 rounded-lg">
          ✓ Analiza technologii i scenariuszy budżetowych zakończona!
        </div>

        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-primary-500 mb-4">
            Podsumowanie Analizy
          </h3>
          <p className="text-gray-300 mb-4">
            Przeanalizowano procesy i przygotowano scenariusze budżetowe z rekomendacjami technologicznymi.
          </p>
          <div className="flex items-center space-x-2 text-gray-400">
            <TrendingUp className="w-5 h-5 text-primary-500" />
            <span>Poziom budżetu: {budgetLevel === 'low' ? 'Niski' : budgetLevel === 'medium' ? 'Średni' : 'Wysoki'}</span>
          </div>
        </div>

        <button onClick={handleComplete} className="btn btn-primary w-full">
          Przejdź do Kroku 4 - Generowanie Prezentacji
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-4">Krok 3: Rekomendacje Technologiczne</h2>

      <div className="bg-dark-800 p-6 rounded-lg space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-primary-500 mb-4">
            Wybierz Preferencje Budżetowe
          </h3>
          <p className="text-gray-400 mb-4">
            Na podstawie wybranego poziomu budżetu przygotujemy odpowiednie scenariusze automatyzacji
            z rekomendacjami technologicznymi i analizą ROI.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            type="button"
            onClick={() => setBudgetLevel('low')}
            className={`p-6 rounded-lg border-2 transition-all ${
              budgetLevel === 'low'
                ? 'border-primary-500 bg-primary-500/10'
                : 'border-dark-600 hover:border-primary-500'
            }`}
          >
            <DollarSign className="w-10 h-10 text-primary-500 mb-3 mx-auto" />
            <h4 className="font-semibold text-white mb-2">Niski Budżet</h4>
            <p className="text-sm text-gray-400">
              Rozwiązania ekonomiczne, automatyzacja 50-70% procesów
            </p>
          </button>

          <button
            type="button"
            onClick={() => setBudgetLevel('medium')}
            className={`p-6 rounded-lg border-2 transition-all ${
              budgetLevel === 'medium'
                ? 'border-primary-500 bg-primary-500/10'
                : 'border-dark-600 hover:border-primary-500'
            }`}
          >
            <DollarSign className="w-10 h-10 text-primary-500 mb-3 mx-auto" />
            <DollarSign className="w-10 h-10 text-primary-500 mb-3 mx-auto -mt-10" />
            <h4 className="font-semibold text-white mb-2">Średni Budżet</h4>
            <p className="text-sm text-gray-400">
              Rozwiązania średniej klasy, automatyzacja 70-90% procesów
            </p>
          </button>

          <button
            type="button"
            onClick={() => setBudgetLevel('high')}
            className={`p-6 rounded-lg border-2 transition-all ${
              budgetLevel === 'high'
                ? 'border-primary-500 bg-primary-500/10'
                : 'border-dark-600 hover:border-primary-500'
            }`}
          >
            <DollarSign className="w-10 h-10 text-primary-500 mb-3 mx-auto" />
            <DollarSign className="w-10 h-10 text-primary-500 mb-3 mx-auto -mt-10" />
            <DollarSign className="w-10 h-10 text-primary-500 mb-3 mx-auto -mt-10" />
            <h4 className="font-semibold text-white mb-2">Wysoki Budżet</h4>
            <p className="text-sm text-gray-400">
              Rozwiązania enterprise, pełna automatyzacja 90-100%
            </p>
          </button>
        </div>

        <div className="bg-dark-700 p-4 rounded-lg">
          <h4 className="font-semibold text-white mb-2">Co zostanie przeanalizowane:</h4>
          <ul className="space-y-2 text-gray-300">
            <li className="flex items-start space-x-2">
              <span className="text-primary-500">•</span>
              <span>Research technologii automatyzacyjnych (RPA, BPM, AI/ML, IDP, iPaaS)</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-primary-500">•</span>
              <span>Ocena vendorów i rozwiązań dostępnych na rynku</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-primary-500">•</span>
              <span>3 scenariusze budżetowe z analizą CAPEX i OPEX</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-primary-500">•</span>
              <span>Projektowanie procesu TO-BE dla każdego scenariusza</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-primary-500">•</span>
              <span>Kalkulacja ROI, payback period i NPV</span>
            </li>
          </ul>
        </div>
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
        {isLoading ? (
          <>
            <Loader className="w-5 h-5 animate-spin" />
            <span>Wykonywanie analizy technologicznej... (może potrwać kilka minut)</span>
          </>
        ) : (
          <span>Wykonaj Research i Analizę</span>
        )}
      </button>
    </form>
  );
}
