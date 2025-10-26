import { useState, useEffect } from 'react';
import { Plus, Loader, ChevronDown, ChevronUp } from 'lucide-react';
import { step1API, step2API } from '../services/api';
import type { Step2ProcessData, Step1Result } from '../types';

interface Step2FormProps {
  projectId: number;
  onComplete: () => void;
}

export default function Step2Form({ projectId, onComplete }: Step2FormProps) {
  const [topProcesses, setTopProcesses] = useState<string[]>([]);
  const [selectedProcess, setSelectedProcess] = useState<string>('');
  const [processId, setProcessId] = useState<number | null>(null);
  const [formData, setFormData] = useState<Step2ProcessData>({
    basic_info: {
      name: '',
      department: '',
      process_owner: '',
      objective: '',
      scope: '',
    },
    as_is: {
      steps: [],
      total_cycle_time_hours: 0,
      execution_frequency: '',
      annual_volume: 0,
      fte_count: 0,
    },
    costs: {
      labor_costs: 0,
      operational_costs: 0,
      error_costs: 0,
      delay_costs: 0,
    },
    problems: {
      problems: [],
    },
    systems: {
      systems_used: [],
      integrations: [],
      data_quality: '',
      technical_bottlenecks: [],
    },
  });
  const [results, setResults] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [analyzedProcesses, setAnalyzedProcesses] = useState<string[]>([]);

  useEffect(() => {
    loadStep1Results();
  }, [projectId]);

  const loadStep1Results = async () => {
    try {
      const step1Results: Step1Result = await step1API.getResults(projectId);
      setTopProcesses(step1Results.top_processes);
    } catch (error) {
      console.error('Error loading Step 1 results:', error);
    }
  };

  const handleProcessSelect = async (processName: string) => {
    setSelectedProcess(processName);
    setFormData({
      ...formData,
      basic_info: { ...formData.basic_info, name: processName },
    });
    
    // Create process entry
    try {
      const response = await step2API.addProcess(projectId, processName);
      setProcessId(response.id);
    } catch (error) {
      console.error('Error adding process:', error);
    }
  };

  const handleAddStep = () => {
    setFormData({
      ...formData,
      as_is: {
        ...formData.as_is,
        steps: [
          ...formData.as_is.steps,
          {
            name: '',
            description: '',
            executor: '',
            system_used: '',
            duration_minutes: 0,
            frequency: '',
            action_type: 'manual',
          },
        ],
      },
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!processId) return;

    setIsLoading(true);
    try {
      // Update process data
      await step2API.updateProcess(projectId, processId, formData);
      
      // Analyze process
      const analysisResults = await step2API.analyzeProcess(projectId, processId);
      setResults(analysisResults);
      setShowResults(true);
      
      // Mark as analyzed
      setAnalyzedProcesses([...analyzedProcesses, selectedProcess]);
      
      // Reset for next process
      setSelectedProcess('');
      setProcessId(null);
    } catch (error) {
      console.error('Error analyzing process:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCompleteStep = () => {
    onComplete();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-4">Krok 2: Mapowanie Procesów</h2>

      {/* Process Selection */}
      <div className="bg-dark-800 p-6 rounded-lg">
        <h3 className="text-lg font-semibold text-primary-500 mb-4">
          Wybierz Proces do Analizy
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {topProcesses.map((process) => {
            const isAnalyzed = analyzedProcesses.includes(process);
            return (
              <button
                key={process}
                onClick={() => !isAnalyzed && handleProcessSelect(process)}
                disabled={isAnalyzed}
                className={`p-4 rounded-lg border-2 transition-all text-left ${
                  selectedProcess === process
                    ? 'border-primary-500 bg-primary-500/10'
                    : isAnalyzed
                    ? 'border-green-500 bg-green-500/10 cursor-not-allowed'
                    : 'border-dark-600 hover:border-primary-500'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-white">{process}</span>
                  {isAnalyzed && <span className="text-green-500 text-sm">✓ Przeanalizowany</span>}
                </div>
              </button>
            );
          })}
        </div>
        
        <div className="mt-4 flex items-center justify-between">
          <div className="text-sm text-gray-400">
            Przeanalizowano: {analyzedProcesses.length} / {topProcesses.length}
          </div>
          {analyzedProcesses.length === topProcesses.length && (
            <button onClick={handleCompleteStep} className="btn btn-primary">
              Przejdź do Kroku 3
            </button>
          )}
        </div>
      </div>

      {/* Process Form */}
      {selectedProcess && !showResults && (
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h3 className="text-lg font-semibold text-primary-500">Informacje Podstawowe</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Dział odpowiedzialny</label>
                <input
                  type="text"
                  value={formData.basic_info.department}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      basic_info: { ...formData.basic_info, department: e.target.value },
                    })
                  }
                  className="input"
                  required
                />
              </div>
              
              <div>
                <label className="label">Process Owner</label>
                <input
                  type="text"
                  value={formData.basic_info.process_owner}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      basic_info: { ...formData.basic_info, process_owner: e.target.value },
                    })
                  }
                  className="input"
                  required
                />
              </div>
            </div>

            <div>
              <label className="label">Cel procesu</label>
              <textarea
                value={formData.basic_info.objective}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    basic_info: { ...formData.basic_info, objective: e.target.value },
                  })
                }
                className="input"
                rows={2}
                required
              />
            </div>

            <div>
              <label className="label">Zakres procesu</label>
              <textarea
                value={formData.basic_info.scope}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    basic_info: { ...formData.basic_info, scope: e.target.value },
                  })
                }
                className="input"
                rows={2}
                required
              />
            </div>
          </div>

          {/* AS-IS Steps */}
          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h3 className="text-lg font-semibold text-primary-500">Kroki Procesu (AS-IS)</h3>
            
            {formData.as_is.steps.map((step, index) => (
              <div key={index} className="bg-dark-700 p-4 rounded-lg space-y-3">
                <h4 className="font-semibold text-white">Krok {index + 1}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <input
                    type="text"
                    placeholder="Nazwa kroku"
                    value={step.name}
                    onChange={(e) => {
                      const newSteps = [...formData.as_is.steps];
                      newSteps[index].name = e.target.value;
                      setFormData({ ...formData, as_is: { ...formData.as_is, steps: newSteps } });
                    }}
                    className="input"
                    required
                  />
                  <input
                    type="text"
                    placeholder="Wykonawca (rola)"
                    value={step.executor}
                    onChange={(e) => {
                      const newSteps = [...formData.as_is.steps];
                      newSteps[index].executor = e.target.value;
                      setFormData({ ...formData, as_is: { ...formData.as_is, steps: newSteps } });
                    }}
                    className="input"
                    required
                  />
                  <input
                    type="text"
                    placeholder="System wykorzystywany"
                    value={step.system_used}
                    onChange={(e) => {
                      const newSteps = [...formData.as_is.steps];
                      newSteps[index].system_used = e.target.value;
                      setFormData({ ...formData, as_is: { ...formData.as_is, steps: newSteps } });
                    }}
                    className="input"
                    required
                  />
                  <input
                    type="number"
                    placeholder="Czas trwania (minuty)"
                    value={step.duration_minutes}
                    onChange={(e) => {
                      const newSteps = [...formData.as_is.steps];
                      newSteps[index].duration_minutes = parseInt(e.target.value) || 0;
                      setFormData({ ...formData, as_is: { ...formData.as_is, steps: newSteps } });
                    }}
                    className="input"
                    required
                  />
                </div>
              </div>
            ))}
            
            <button
              type="button"
              onClick={handleAddStep}
              className="btn btn-secondary flex items-center space-x-2"
            >
              <Plus className="w-5 h-5" />
              <span>Dodaj Krok</span>
            </button>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label className="label">Całkowity czas cyklu (godziny)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.as_is.total_cycle_time_hours}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      as_is: { ...formData.as_is, total_cycle_time_hours: parseFloat(e.target.value) || 0 },
                    })
                  }
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Częstotliwość wykonywania</label>
                <input
                  type="text"
                  placeholder="np. dziennie, tygodniowo"
                  value={formData.as_is.execution_frequency}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      as_is: { ...formData.as_is, execution_frequency: e.target.value },
                    })
                  }
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Liczba transakcji (rocznie)</label>
                <input
                  type="number"
                  value={formData.as_is.annual_volume}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      as_is: { ...formData.as_is, annual_volume: parseInt(e.target.value) || 0 },
                    })
                  }
                  className="input"
                  required
                />
              </div>
            </div>
          </div>

          {/* Costs */}
          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h3 className="text-lg font-semibold text-primary-500">Koszty i Zasoby</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Koszty pracownicze (PLN/rok)</label>
                <input
                  type="number"
                  value={formData.costs.labor_costs}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      costs: { ...formData.costs, labor_costs: parseFloat(e.target.value) || 0 },
                    })
                  }
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Koszty operacyjne (PLN/rok)</label>
                <input
                  type="number"
                  value={formData.costs.operational_costs}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      costs: { ...formData.costs, operational_costs: parseFloat(e.target.value) || 0 },
                    })
                  }
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Koszty błędów (PLN/rok)</label>
                <input
                  type="number"
                  value={formData.costs.error_costs}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      costs: { ...formData.costs, error_costs: parseFloat(e.target.value) || 0 },
                    })
                  }
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Koszty opóźnień (PLN/rok)</label>
                <input
                  type="number"
                  value={formData.costs.delay_costs}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      costs: { ...formData.costs, delay_costs: parseFloat(e.target.value) || 0 },
                    })
                  }
                  className="input"
                  required
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="btn btn-primary w-full flex items-center justify-center space-x-2"
          >
            {isLoading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Analizowanie procesu...</span>
              </>
            ) : (
              <span>Analizuj Proces</span>
            )}
          </button>
        </form>
      )}

      {/* Results */}
      {showResults && results && (
        <div className="bg-dark-800 p-6 rounded-lg space-y-4">
          <h3 className="text-lg font-semibold text-primary-500">Wyniki Analizy</h3>
          
          <div className="bg-green-500/10 border border-green-500 text-green-500 px-4 py-2 rounded-lg">
            ✓ Proces przeanalizowany pomyślnie!
          </div>

          <div>
            <h4 className="font-semibold text-white mb-2">Potencjał Automatyzacji</h4>
            <div className="text-3xl font-bold text-primary-500">
              {results.automation_potential.percentage}%
            </div>
          </div>

          <button
            onClick={() => {
              setShowResults(false);
              setResults(null);
            }}
            className="btn btn-primary"
          >
            Analizuj Kolejny Proces
          </button>
        </div>
      )}
    </div>
  );
}
