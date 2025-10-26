import { useState } from 'react';
import { Plus, Minus, Loader } from 'lucide-react';
import { step1API } from '../services/api';
import type { Step1Input, Step1Result } from '../types';

interface Step1FormProps {
  projectId: number;
  onComplete: () => void;
}

export default function Step1Form({ projectId, onComplete }: Step1FormProps) {
  const [formData, setFormData] = useState<Step1Input>({
    organization_data: {
      company_name: '',
      industry: '',
      size: '',
      structure: '',
      description: '',
    },
    questionnaire_answers: {},
    processes_list: [''],
  });
  const [results, setResults] = useState<Step1Result | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const questions = [
    { id: 'process_documentation', label: 'Czy procesy biznesowe są udokumentowane?', type: 'scale' },
    { id: 'process_standardization', label: 'Stopień standaryzacji procesów (1-10)', type: 'scale' },
    { id: 'digital_systems', label: 'Liczba systemów IT wykorzystywanych w organizacji', type: 'number' },
    { id: 'data_quality', label: 'Jakość danych w systemach (1-10)', type: 'scale' },
    { id: 'it_infrastructure', label: 'Stan infrastruktury IT (1-10)', type: 'scale' },
    { id: 'change_readiness', label: 'Gotowość organizacji na zmiany (1-10)', type: 'scale' },
    { id: 'leadership_support', label: 'Wsparcie kierownictwa dla automatyzacji (1-10)', type: 'scale' },
    { id: 'budget_availability', label: 'Dostępny budżet na automatyzację (PLN)', type: 'number' },
  ];

  const handleAddProcess = () => {
    setFormData({
      ...formData,
      processes_list: [...formData.processes_list, ''],
    });
  };

  const handleRemoveProcess = (index: number) => {
    setFormData({
      ...formData,
      processes_list: formData.processes_list.filter((_, i) => i !== index),
    });
  };

  const handleProcessChange = (index: number, value: string) => {
    const newList = [...formData.processes_list];
    newList[index] = value;
    setFormData({ ...formData, processes_list: newList });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const result = await step1API.analyze(projectId, formData);
      setResults(result);
      setTimeout(() => {
        onComplete();
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd analizy');
    } finally {
      setIsLoading(false);
    }
  };

  if (results) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white mb-4">Wyniki Analizy Wstępnej</h2>

        {/* Digital Maturity */}
        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-primary-500 mb-4">Dojrzałość Cyfrowa</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
            <div>
              <div className="text-sm text-gray-400">Process Maturity</div>
              <div className="text-2xl font-bold text-white">{results.digital_maturity.process_maturity}/100</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Digital Infrastructure</div>
              <div className="text-2xl font-bold text-white">{results.digital_maturity.digital_infrastructure}/100</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Data Quality</div>
              <div className="text-2xl font-bold text-white">{results.digital_maturity.data_quality}/100</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Organizational Readiness</div>
              <div className="text-2xl font-bold text-white">{results.digital_maturity.organizational_readiness}/100</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Financial Capacity</div>
              <div className="text-2xl font-bold text-white">{results.digital_maturity.financial_capacity}/100</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Strategic Alignment</div>
              <div className="text-2xl font-bold text-white">{results.digital_maturity.strategic_alignment}/100</div>
            </div>
          </div>
          <div className="bg-dark-700 p-4 rounded-lg">
            <div className="text-lg font-semibold text-primary-500 mb-2">
              Overall Score: {results.digital_maturity.overall_score}/100
            </div>
            <p className="text-gray-300">{results.digital_maturity.interpretation}</p>
          </div>
        </div>

        {/* Top Processes */}
        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-primary-500 mb-4">
            TOP {results.top_processes.length} Procesów do Automatyzacji
          </h3>
          <ul className="space-y-2">
            {results.top_processes.map((process, index) => (
              <li key={index} className="flex items-center space-x-3">
                <span className="flex-shrink-0 w-8 h-8 bg-primary-500 text-dark-900 rounded-full flex items-center justify-center font-bold">
                  {index + 1}
                </span>
                <span className="text-white">{process}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Recommendations */}
        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-primary-500 mb-4">Rekomendacje</h3>
          <p className="text-gray-300 whitespace-pre-wrap">{results.recommendations}</p>
        </div>

        <div className="bg-primary-500/10 border border-primary-500 p-4 rounded-lg text-primary-500">
          ✓ Analiza zakończona. Przejście do Kroku 2...
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-4">Krok 1: Analiza Wstępna</h2>

      {/* Organization Data */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-primary-500">Dane Organizacji</h3>
        
        <div>
          <label className="label">Nazwa firmy</label>
          <input
            type="text"
            value={formData.organization_data.company_name}
            onChange={(e) =>
              setFormData({
                ...formData,
                organization_data: { ...formData.organization_data, company_name: e.target.value },
              })
            }
            className="input"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="label">Branża</label>
            <input
              type="text"
              value={formData.organization_data.industry}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  organization_data: { ...formData.organization_data, industry: e.target.value },
                })
              }
              className="input"
              required
            />
          </div>

          <div>
            <label className="label">Wielkość</label>
            <select
              value={formData.organization_data.size}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  organization_data: { ...formData.organization_data, size: e.target.value },
                })
              }
              className="input"
              required
            >
              <option value="">Wybierz...</option>
              <option value="small">Mała (1-50 pracowników)</option>
              <option value="medium">Średnia (51-250 pracowników)</option>
              <option value="large">Duża (251+ pracowników)</option>
            </select>
          </div>

          <div>
            <label className="label">Struktura</label>
            <input
              type="text"
              value={formData.organization_data.structure}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  organization_data: { ...formData.organization_data, structure: e.target.value },
                })
              }
              className="input"
              required
            />
          </div>
        </div>

        <div>
          <label className="label">Opis (opcjonalnie)</label>
          <textarea
            value={formData.organization_data.description}
            onChange={(e) =>
              setFormData({
                ...formData,
                organization_data: { ...formData.organization_data, description: e.target.value },
              })
            }
            className="input"
            rows={3}
          />
        </div>
      </div>

      {/* Questionnaire */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-primary-500">Kwestionariusz Diagnostyczny</h3>
        {questions.map((question) => (
          <div key={question.id}>
            <label className="label">{question.label}</label>
            {question.type === 'scale' ? (
              <input
                type="range"
                min="1"
                max="10"
                value={formData.questionnaire_answers[question.id] || 5}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    questionnaire_answers: {
                      ...formData.questionnaire_answers,
                      [question.id]: parseInt(e.target.value),
                    },
                  })
                }
                className="w-full"
              />
            ) : (
              <input
                type="number"
                value={formData.questionnaire_answers[question.id] || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    questionnaire_answers: {
                      ...formData.questionnaire_answers,
                      [question.id]: parseInt(e.target.value) || 0,
                    },
                  })
                }
                className="input"
              />
            )}
            {question.type === 'scale' && (
              <div className="text-sm text-gray-400 mt-1">
                Wartość: {formData.questionnaire_answers[question.id] || 5}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Processes List */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-primary-500">Lista Procesów Biznesowych</h3>
        {formData.processes_list.map((process, index) => (
          <div key={index} className="flex space-x-2">
            <input
              type="text"
              value={process}
              onChange={(e) => handleProcessChange(index, e.target.value)}
              className="input flex-1"
              placeholder={`Proces ${index + 1}`}
              required
            />
            {formData.processes_list.length > 1 && (
              <button
                type="button"
                onClick={() => handleRemoveProcess(index)}
                className="btn btn-secondary"
              >
                <Minus className="w-5 h-5" />
              </button>
            )}
          </div>
        ))}
        <button
          type="button"
          onClick={handleAddProcess}
          className="btn btn-secondary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Dodaj Proces</span>
        </button>
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
            <span>Analizowanie...</span>
          </>
        ) : (
          <span>Analizuj i Przejdź do Kroku 2</span>
        )}
      </button>
    </form>
  );
}
