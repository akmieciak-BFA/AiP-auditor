import { useState, useEffect } from 'react';
import { Loader, FileText, ExternalLink } from 'lucide-react';
import { step4API, step1API } from '../services/api';

interface Step4FormProps {
  projectId: number;
  onComplete: () => void;
}

export default function Step4Form({ projectId, onComplete }: Step4FormProps) {
  const [formData, setFormData] = useState({
    client_name: '',
    author_name: '',
    selected_processes: [] as string[],
    budget_scenario: 'medium',
  });
  const [availableProcesses, setAvailableProcesses] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [generatedUrl, setGeneratedUrl] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadAvailableProcesses();
  }, [projectId]);

  const loadAvailableProcesses = async () => {
    try {
      const step1Results = await step1API.getResults(projectId);
      setAvailableProcesses(step1Results.top_processes);
      setFormData({
        ...formData,
        selected_processes: step1Results.top_processes,
      });
    } catch (error) {
      console.error('Error loading processes:', error);
    }
  };

  const handleProcessToggle = (process: string) => {
    if (formData.selected_processes.includes(process)) {
      setFormData({
        ...formData,
        selected_processes: formData.selected_processes.filter((p) => p !== process),
      });
    } else {
      setFormData({
        ...formData,
        selected_processes: [...formData.selected_processes, process],
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await step4API.generatePresentation(projectId, formData);
      setGeneratedUrl(response.gamma_url);
      onComplete();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd generowania prezentacji');
    } finally {
      setIsLoading(false);
    }
  };

  if (generatedUrl) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white mb-4">Prezentacja Wygenerowana!</h2>

        <div className="bg-primary-500/10 border border-primary-500 text-primary-500 px-6 py-4 rounded-lg">
          <div className="flex items-center space-x-3 mb-3">
            <FileText className="w-8 h-8" />
            <div>
              <h3 className="font-semibold text-lg">Audyt automatyzacyjny - {formData.client_name}</h3>
              <p className="text-sm">przez {formData.author_name}</p>
            </div>
          </div>
          <a
            href={generatedUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary flex items-center justify-center space-x-2 w-full"
          >
            <ExternalLink className="w-5 h-5" />
            <span>Otwórz Prezentację</span>
          </a>
        </div>

        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-4">Podsumowanie Audytu</h3>
          <div className="space-y-3 text-gray-300">
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Klient:</span>
              <span className="font-semibold">{formData.client_name}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Autor:</span>
              <span className="font-semibold">{formData.author_name}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Liczba procesów:</span>
              <span className="font-semibold">{formData.selected_processes.length}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Scenariusz budżetowy:</span>
              <span className="font-semibold">
                {formData.budget_scenario === 'low' ? 'Niski' : formData.budget_scenario === 'medium' ? 'Średni' : 'Wysoki'}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-green-500/10 border border-green-500 text-green-500 px-4 py-2 rounded-lg">
          ✓ Projekt audytowy zakończony pomyślnie!
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-4">Krok 4: Generowanie Prezentacji</h2>

      <div className="bg-dark-800 p-6 rounded-lg space-y-4">
        <h3 className="text-lg font-semibold text-primary-500">Ustawienia Prezentacji</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label">Nazwa klienta</label>
            <input
              type="text"
              value={formData.client_name}
              onChange={(e) => setFormData({ ...formData, client_name: e.target.value })}
              className="input"
              placeholder="np. ACME Corporation"
              required
            />
          </div>

          <div>
            <label className="label">Autor audytu</label>
            <input
              type="text"
              value={formData.author_name}
              onChange={(e) => setFormData({ ...formData, author_name: e.target.value })}
              className="input"
              placeholder="np. Jan Kowalski"
              required
            />
          </div>
        </div>

        <div>
          <label className="label">Scenariusz budżetowy</label>
          <select
            value={formData.budget_scenario}
            onChange={(e) => setFormData({ ...formData, budget_scenario: e.target.value })}
            className="input"
            required
          >
            <option value="low">Niski budżet (Budget-Conscious)</option>
            <option value="medium">Średni budżet (Strategic Implementation)</option>
            <option value="high">Wysoki budżet (Enterprise Transformation)</option>
          </select>
        </div>
      </div>

      <div className="bg-dark-800 p-6 rounded-lg space-y-4">
        <h3 className="text-lg font-semibold text-primary-500">Wybierz Procesy do Uwzględnienia</h3>
        <div className="space-y-2">
          {availableProcesses.map((process) => (
            <label
              key={process}
              className="flex items-center space-x-3 p-3 bg-dark-700 rounded-lg cursor-pointer hover:bg-dark-600 transition-colors"
            >
              <input
                type="checkbox"
                checked={formData.selected_processes.includes(process)}
                onChange={() => handleProcessToggle(process)}
                className="w-5 h-5 text-primary-500 bg-dark-700 border-dark-600 rounded focus:ring-primary-500"
              />
              <span className="text-white">{process}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="bg-dark-800 p-6 rounded-lg">
        <h3 className="text-lg font-semibold text-primary-500 mb-4">Co zostanie wygenerowane:</h3>
        <ul className="space-y-2 text-gray-300">
          <li className="flex items-start space-x-2">
            <span className="text-primary-500">•</span>
            <span>Profesjonalna prezentacja zgodna ze stylem BFA (ciemny granatowy, zielone akcenty)</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="text-primary-500">•</span>
            <span>Wprowadzenie z 5 kluczowymi wartościami audytu</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="text-primary-500">•</span>
            <span>Metodologia audytu (3 fazy)</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="text-primary-500">•</span>
            <span>TOP procesów do automatyzacji</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="text-primary-500">•</span>
            <span>Szczegółowa analiza każdego procesu (AS-IS, MUDA, wąskie gardła, TO-BE)</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="text-primary-500">•</span>
            <span>Podsumowanie i rekomendacje</span>
          </li>
        </ul>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-2 rounded-lg">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading || formData.selected_processes.length === 0}
        className="btn btn-primary w-full flex items-center justify-center space-x-2"
      >
        {isLoading ? (
          <>
            <Loader className="w-5 h-5 animate-spin" />
            <span>Generowanie prezentacji...</span>
          </>
        ) : (
          <>
            <FileText className="w-5 h-5" />
            <span>Generuj Prezentację</span>
          </>
        )}
      </button>
    </form>
  );
}
