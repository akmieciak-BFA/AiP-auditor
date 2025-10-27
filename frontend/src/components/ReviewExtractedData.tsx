import { useState, useEffect } from 'react';
import { CheckCircle, AlertTriangle, Edit2, Save } from 'lucide-react';

interface ReviewExtractedDataProps {
  projectId: number;
  processingResultId: number;
  onConfirm: (data: any) => void;
  onBack: () => void;
}

interface ConfidenceScores {
  organization: number;
  digital_maturity: number;
  pain_points: number;
  goals: number;
  budget: number;
  timeline: number;
  resources: number;
  constraints: number;
  processes_identified: number;
}

export default function ReviewExtractedData({
  projectId,
  processingResultId,
  onConfirm,
  onBack
}: ReviewExtractedDataProps) {
  const [extractedData, setExtractedData] = useState<any>(null);
  const [confidenceScores, setConfidenceScores] = useState<ConfidenceScores | null>(null);
  const [missingFields, setMissingFields] = useState<any[]>([]);
  const [processingSummary, setProcessingSummary] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [editMode, setEditMode] = useState<Record<string, boolean>>({});

  useEffect(() => {
    fetchExtractedData();
  }, [projectId, processingResultId]);

  const fetchExtractedData = async () => {
    try {
      // Fetch latest analysis from new endpoint
      const response = await fetch(
        `http://localhost:8000/api/projects/${projectId}/documents/latest-analysis`
      );
      
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const result = await response.json();
      
      if (!result.has_analysis) {
        throw new Error('No analysis available');
      }
      
      // New BFA format
      setExtractedData(result.extracted_data || {});
      setConfidenceScores(result.confidence_scores || {});
      setMissingFields(result.missing_fields || []);
      setProcessingSummary(result.processing_summary || {});
    } catch (error) {
      console.error('Error fetching extracted data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-500';
    if (score >= 0.6) return 'text-yellow-500';
    if (score >= 0.4) return 'text-orange-500';
    return 'text-red-500';
  };

  const getConfidenceLabel = (score: number) => {
    if (score >= 0.8) return 'Wysoka pewność';
    if (score >= 0.6) return 'Średnia pewność';
    if (score >= 0.4) return 'Niska pewność';
    return 'Brak danych';
  };

  const getDataQualityBadge = (quality: string) => {
    const colors = {
      excellent: 'bg-green-500/20 text-green-500',
      good: 'bg-blue-500/20 text-blue-500',
      fair: 'bg-yellow-500/20 text-yellow-500',
      poor: 'bg-red-500/20 text-red-500'
    };
    const labels = {
      excellent: 'Doskonała',
      good: 'Dobra',
      fair: 'Średnia',
      poor: 'Słaba'
    };
    
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${colors[quality as keyof typeof colors] || colors.fair}`}>
        {labels[quality as keyof typeof labels] || quality}
      </span>
    );
  };

  const handleFieldUpdate = (section: string, field: string, value: any) => {
    setExtractedData((prev: any) => ({
      ...prev,
      [field]: value
    }));
  };

  const handleConfirm = () => {
    onConfirm(extractedData);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Ładowanie wyciągniętych danych...</div>
      </div>
    );
  }

  const overallConfidence = confidenceScores 
    ? Object.values(confidenceScores).reduce((a, b) => a + b, 0) / Object.values(confidenceScores).length
    : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-dark-800 p-6 rounded-lg">
        <h2 className="text-2xl font-bold text-white mb-2">
          Przegląd wyciągniętych danych
        </h2>
        <p className="text-gray-400">
          Claude przeanalizował Państwa dokumenty. Proszę sprawdzić i uzupełnić dane przed przejściem do analizy.
        </p>
      </div>

      {/* Processing Summary */}
      {processingSummary && (
        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-4">Podsumowanie przetwarzania</h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div>
              <div className="text-sm text-gray-400">Przeanalizowanych dokumentów</div>
              <div className="text-2xl font-bold text-white">{processingSummary.documents_analyzed || 0}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Całkowita liczba stron</div>
              <div className="text-2xl font-bold text-white">{processingSummary.total_pages || 0}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Jakość danych</div>
              <div className="mt-1">{getDataQualityBadge(processingSummary.data_quality)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Pewność ogólna</div>
              <div className={`text-2xl font-bold ${getConfidenceColor(overallConfidence)}`}>
                {(overallConfidence * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          {processingSummary.key_findings && processingSummary.key_findings.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-semibold text-gray-300 mb-2">Kluczowe ustalenia:</h4>
              <ul className="space-y-1">
                {processingSummary.key_findings.map((finding: string, index: number) => (
                  <li key={index} className="text-sm text-gray-400 flex items-start">
                    <CheckCircle className="w-4 h-4 text-primary-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span>{finding}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Confidence Scores by Section */}
      {confidenceScores && (
        <div className="bg-dark-800 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-4">Pewność danych według sekcji</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(confidenceScores).map(([section, score]) => (
              <div key={section} className="bg-dark-700 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-300 capitalize">
                    {section.replace(/_/g, ' ')}
                  </span>
                  <span className={`text-lg font-bold ${getConfidenceColor(score)}`}>
                    {(score * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="w-full bg-dark-600 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      score >= 0.8 ? 'bg-green-500' :
                      score >= 0.6 ? 'bg-yellow-500' :
                      score >= 0.4 ? 'bg-orange-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${score * 100}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {getConfidenceLabel(score)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Missing Fields Alert */}
      {missingFields && missingFields.length > 0 && (
        <div className="bg-yellow-500/10 border border-yellow-500 rounded-lg p-6">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-6 h-6 text-yellow-500 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-yellow-500 mb-2">
                Brakujące dane ({missingFields.length} pól)
              </h3>
              <p className="text-sm text-gray-300 mb-4">
                Następujące pola nie zostały znalezione w dokumentach i wymagają ręcznego uzupełnienia:
              </p>
              
              <div className="space-y-3">
                {missingFields.map((field, index) => (
                  <div key={index} className="bg-dark-800 p-4 rounded-lg">
                    <div className="text-sm font-semibold text-white mb-1">
                      {field.field}
                    </div>
                    <div className="text-xs text-gray-400 mb-2">
                      Powód: {field.reason}
                    </div>
                    <div className="text-sm text-gray-300">
                      Sugerowane pytanie: <span className="italic">"{field.suggested_question}"</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* BFA Analysis Results */}
      {extractedData && (
        <>
          {/* Digital Maturity */}
          {extractedData.digital_maturity && (
            <div className="bg-dark-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">Ocena Dojrzałości Cyfrowej</h3>
              
              <div className="mb-4">
                <div className="text-3xl font-bold text-primary-500 mb-2">
                  {extractedData.digital_maturity.overall_score}/100
                </div>
                <p className="text-sm text-gray-400">
                  {extractedData.digital_maturity.interpretation}
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {Object.entries(extractedData.digital_maturity).map(([key, value]) => {
                  if (key === 'overall_score' || key === 'interpretation') return null;
                  return (
                    <div key={key} className="bg-dark-700 p-3 rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-300 capitalize">
                          {key.replace(/_/g, ' ')}
                        </span>
                        <span className="text-lg font-bold text-primary-500">
                          {value}/100
                        </span>
                      </div>
                      <div className="w-full bg-dark-600 rounded-full h-2">
                        <div
                          className="bg-primary-500 h-2 rounded-full"
                          style={{ width: `${value}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TOP Processes */}
          {extractedData.top_processes && extractedData.top_processes.length > 0 && (
            <div className="bg-dark-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">
                TOP Procesy do Automatyzacji
              </h3>
              <p className="text-sm text-gray-400 mb-4">
                Claude zidentyfikował następujące procesy jako najlepsze kandydaty do automatyzacji:
              </p>
              
              <div className="space-y-2">
                {extractedData.top_processes.map((process: string, index: number) => (
                  <div key={index} className="bg-dark-700 p-4 rounded-lg flex items-center space-x-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
                      <span className="text-white font-bold">{index + 1}</span>
                    </div>
                    <div className="flex-1">
                      <span className="text-white font-medium">{process}</span>
                    </div>
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Processes Scoring */}
          {extractedData.processes_scoring && extractedData.processes_scoring.length > 0 && (
            <div className="bg-dark-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">
                Szczegółowy Scoring Procesów
              </h3>
              
              <div className="space-y-3">
                {extractedData.processes_scoring.map((proc: any, index: number) => (
                  <div key={index} className="bg-dark-700 p-4 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <h4 className="text-white font-semibold">{proc.process_name}</h4>
                        <span className={`text-xs px-2 py-1 rounded ${
                          proc.tier === 1 ? 'bg-green-500/20 text-green-500' :
                          proc.tier === 2 ? 'bg-blue-500/20 text-blue-500' :
                          proc.tier === 3 ? 'bg-yellow-500/20 text-yellow-500' :
                          'bg-red-500/20 text-red-500'
                        }`}>
                          Tier {proc.tier}
                        </span>
                      </div>
                      <div className="text-2xl font-bold text-primary-500">
                        {proc.score}/100
                      </div>
                    </div>
                    <p className="text-sm text-gray-400 mb-2">{proc.rationale}</p>
                    {proc.time_consumption && (
                      <div className="text-xs text-gray-500">
                        Czas: {proc.time_consumption} | Błędy: {proc.error_rate || 'N/A'} | Wolumen: {proc.volume || 'N/A'}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Key Findings */}
          {extractedData.key_findings && extractedData.key_findings.length > 0 && (
            <div className="bg-dark-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">Kluczowe Ustalenia</h3>
              <ul className="space-y-2">
                {extractedData.key_findings.map((finding: string, index: number) => (
                  <li key={index} className="flex items-start text-gray-300">
                    <CheckCircle className="w-5 h-5 text-primary-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span>{finding}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {extractedData.recommendations && (
            <div className="bg-dark-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-4">Rekomendacje</h3>
              <div className="text-gray-300 whitespace-pre-wrap">
                {extractedData.recommendations}
              </div>
            </div>
          )}
        </>
      )}

      {/* Actions */}
      <div className="flex justify-between items-center">
        <button
          onClick={onBack}
          className="btn btn-secondary"
        >
          ← Wróć i prześlij inne pliki
        </button>
        <button
          onClick={handleConfirm}
          className="btn btn-primary flex items-center space-x-2"
        >
          <CheckCircle className="w-5 h-5" />
          <span>Zatwierdź i przejdź do Analizy</span>
        </button>
      </div>
    </div>
  );
}
