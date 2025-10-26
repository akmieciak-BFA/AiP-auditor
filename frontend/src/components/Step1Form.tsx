import { useState } from 'react';
import { Plus, Minus, Loader, Sparkles } from 'lucide-react';
import { step1API } from '../services/api';
import type { Step1Input, Step1Result } from '../types';

interface Step1FormProps {
  projectId: number;
  onComplete: () => void;
}

interface QuestionField {
  id: string;
  category: string;
  question: string;
  type: 'text' | 'number' | 'scale' | 'select' | 'multiselect';
  required: boolean;
  placeholder?: string;
  options?: string[];
  min?: number;
  max?: number;
  help_text?: string;
}

interface DynamicForm {
  questionnaire: QuestionField[];
  process_suggestions: string[];
}

export default function Step1Form({ projectId, onComplete }: Step1FormProps) {
  const [step, setStep] = useState<'org-data' | 'form-generation' | 'questionnaire' | 'results'>('org-data');
  const [orgData, setOrgData] = useState({
    company_name: '',
    industry: '',
    size: '',
    structure: '',
    description: '',
  });
  const [dynamicForm, setDynamicForm] = useState<DynamicForm | null>(null);
  const [formAnswers, setFormAnswers] = useState<Record<string, any>>({});
  const [processesList, setProcessesList] = useState<string[]>(['']);
  const [results, setResults] = useState<Step1Result | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleOrgDataSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    setStep('form-generation');

    try {
      const generatedForm = await step1API.generateForm(projectId, orgData);
      setDynamicForm(generatedForm);
      
      // Add suggested processes
      if (generatedForm.process_suggestions && generatedForm.process_suggestions.length > 0) {
        setProcessesList([...generatedForm.process_suggestions, '']);
      }
      
      setStep('questionnaire');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd generowania formularza');
      setStep('org-data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuestionnaireSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    const formData: Step1Input = {
      organization_data: orgData,
      questionnaire_answers: formAnswers,
      processes_list: processesList.filter(p => p.trim() !== ''),
    };

    try {
      const result = await step1API.analyze(projectId, formData);
      setResults(result);
      setStep('results');
      setTimeout(() => {
        onComplete();
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd analizy');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswerChange = (questionId: string, value: any) => {
    setFormAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleAddProcess = () => {
    setProcessesList([...processesList, '']);
  };

  const handleRemoveProcess = (index: number) => {
    setProcessesList(processesList.filter((_, i) => i !== index));
  };

  const handleProcessChange = (index: number, value: string) => {
    const newList = [...processesList];
    newList[index] = value;
    setProcessesList(newList);
  };

  const renderQuestion = (question: QuestionField) => {
    const value = formAnswers[question.id];

    switch (question.type) {
      case 'text':
        return (
          <textarea
            value={value || ''}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            className="input"
            placeholder={question.placeholder}
            required={question.required}
            rows={3}
          />
        );

      case 'number':
        return (
          <input
            type="number"
            value={value || ''}
            onChange={(e) => handleAnswerChange(question.id, parseFloat(e.target.value) || 0)}
            className="input"
            placeholder={question.placeholder}
            min={question.min}
            max={question.max}
            required={question.required}
          />
        );

      case 'scale':
        return (
          <div className="space-y-2">
            <input
              type="range"
              min={question.min || 1}
              max={question.max || 10}
              value={value || Math.floor(((question.max || 10) + (question.min || 1)) / 2)}
              onChange={(e) => handleAnswerChange(question.id, parseInt(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">{question.min || 1}</span>
              <span className="text-primary-500 font-semibold">
                Wartość: {value || Math.floor(((question.max || 10) + (question.min || 1)) / 2)}
              </span>
              <span className="text-gray-400">{question.max || 10}</span>
            </div>
          </div>
        );

      case 'select':
        return (
          <select
            value={value || ''}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            className="input"
            required={question.required}
          >
            <option value="">Wybierz...</option>
            {question.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );

      case 'multiselect':
        return (
          <div className="space-y-2">
            {question.options?.map((option) => (
              <label
                key={option}
                className="flex items-center space-x-2 p-2 bg-dark-700 rounded cursor-pointer hover:bg-dark-600"
              >
                <input
                  type="checkbox"
                  checked={(value || []).includes(option)}
                  onChange={(e) => {
                    const current = value || [];
                    if (e.target.checked) {
                      handleAnswerChange(question.id, [...current, option]);
                    } else {
                      handleAnswerChange(question.id, current.filter((v: string) => v !== option));
                    }
                  }}
                  className="w-4 h-4 text-primary-500 bg-dark-700 border-dark-600 rounded"
                />
                <span className="text-white">{option}</span>
              </label>
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  // Organization Data Step
  if (step === 'org-data') {
    return (
      <form onSubmit={handleOrgDataSubmit} className="space-y-6">
        <h2 className="text-2xl font-bold text-white mb-4">Krok 1: Analiza Wstępna</h2>
        <p className="text-gray-400 mb-6">
          Podaj podstawowe informacje o organizacji. Na ich podstawie wygenerujemy spersonalizowany kwestionariusz diagnostyczny.
        </p>

        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-primary-500">Dane Organizacji</h3>
          
          <div>
            <label className="label">Nazwa firmy</label>
            <input
              type="text"
              value={orgData.company_name}
              onChange={(e) => setOrgData({ ...orgData, company_name: e.target.value })}
              className="input"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="label">Branża</label>
              <input
                type="text"
                value={orgData.industry}
                onChange={(e) => setOrgData({ ...orgData, industry: e.target.value })}
                className="input"
                placeholder="np. Produkcja, IT, Finanse"
                required
              />
            </div>

            <div>
              <label className="label">Wielkość</label>
              <select
                value={orgData.size}
                onChange={(e) => setOrgData({ ...orgData, size: e.target.value })}
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
              <label className="label">Struktura organizacyjna</label>
              <input
                type="text"
                value={orgData.structure}
                onChange={(e) => setOrgData({ ...orgData, structure: e.target.value })}
                className="input"
                placeholder="np. Funkcjonalna, Macierzowa"
                required
              />
            </div>
          </div>

          <div>
            <label className="label">Opis organizacji (opcjonalnie)</label>
            <textarea
              value={orgData.description}
              onChange={(e) => setOrgData({ ...orgData, description: e.target.value })}
              className="input"
              rows={3}
              placeholder="Krótki opis działalności, specyfiki organizacji..."
            />
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
          <Sparkles className="w-5 h-5" />
          <span>Wygeneruj Spersonalizowany Kwestionariusz</span>
        </button>
      </form>
    );
  }

  // Form Generation Loading
  if (step === 'form-generation') {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4">
        <Loader className="w-16 h-16 text-primary-500 animate-spin" />
        <h3 className="text-xl font-semibold text-white">Generowanie kwestionariusza...</h3>
        <p className="text-gray-400 text-center max-w-md">
          Claude Sonnet 4.5 analizuje Twoją organizację i tworzy spersonalizowane pytania diagnostyczne.
          To może potrwać 30-60 sekund.
        </p>
        <div className="bg-dark-700 p-4 rounded-lg max-w-md">
          <div className="text-sm text-gray-300 space-y-2">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse"></div>
              <span>Analiza branży i wielkości organizacji</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
              <span>Dobór odpowiednich kategorii pytań</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
              <span>Tworzenie spersonalizowanych pytań</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Dynamic Questionnaire
  if (step === 'questionnaire' && dynamicForm) {
    // Group questions by category
    const categories = Array.from(new Set(dynamicForm.questionnaire.map(q => q.category)));

    return (
      <form onSubmit={handleQuestionnaireSubmit} className="space-y-6">
        <div className="bg-primary-500/10 border border-primary-500 p-4 rounded-lg mb-6">
          <div className="flex items-center space-x-2 text-primary-500 mb-2">
            <Sparkles className="w-5 h-5" />
            <span className="font-semibold">Kwestionariusz Spersonalizowany</span>
          </div>
          <p className="text-sm text-gray-300">
            Ten kwestionariusz został wygenerowany specjalnie dla organizacji <strong>{orgData.company_name}</strong> 
            w branży <strong>{orgData.industry}</strong>.
          </p>
        </div>

        {categories.map((category) => {
          const categoryQuestions = dynamicForm.questionnaire.filter(q => q.category === category);
          
          return (
            <div key={category} className="bg-dark-800 p-6 rounded-lg space-y-4">
              <h3 className="text-lg font-semibold text-primary-500">{category}</h3>
              
              {categoryQuestions.map((question) => (
                <div key={question.id} className="space-y-2">
                  <label className="label">
                    {question.question}
                    {question.required && <span className="text-red-500 ml-1">*</span>}
                  </label>
                  {question.help_text && (
                    <p className="text-sm text-gray-400 mb-2">{question.help_text}</p>
                  )}
                  {renderQuestion(question)}
                </div>
              ))}
            </div>
          );
        })}

        {/* Processes List */}
        <div className="bg-dark-800 p-6 rounded-lg space-y-4">
          <div>
            <h3 className="text-lg font-semibold text-primary-500 mb-2">Lista Procesów Biznesowych</h3>
            <p className="text-sm text-gray-400 mb-4">
              Zaproponowaliśmy procesy typowe dla Twojej branży. Możesz je edytować lub dodać własne.
            </p>
          </div>
          
          {processesList.map((process, index) => (
            <div key={index} className="flex space-x-2">
              <input
                type="text"
                value={process}
                onChange={(e) => handleProcessChange(index, e.target.value)}
                className="input flex-1"
                placeholder={`Proces ${index + 1}`}
                required
              />
              {processesList.length > 1 && (
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
              <span>Analizowanie z Extended Thinking...</span>
            </>
          ) : (
            <span>Analizuj i Przejdź do Kroku 2</span>
          )}
        </button>
      </form>
    );
  }

  // Results
  if (step === 'results' && results) {
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

  return null;
}
