import React from 'react';
import { QualityMetrics as QualityMetricsType } from '../types';

interface QualityMetricsProps {
  metrics: QualityMetricsType;
  stepName: string;
}

export const QualityMetrics: React.FC<QualityMetricsProps> = ({ metrics, stepName }) => {
  if (!metrics) return null;

  const totalWords = Object.values(metrics.word_counts).reduce((sum, count) => sum + count, 0);

  return (
    <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-semibold text-gray-900">Metryki Jakości Outputu</h4>
        <div className="flex items-center gap-2">
          {metrics.is_valid ? (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              ✓ Spełnia standardy
            </span>
          ) : (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
              ⚠ Poniżej standardów
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div className="bg-white p-3 rounded border border-gray-200">
          <div className="text-xs text-gray-500 mb-1">Całkowita liczba słów</div>
          <div className="text-2xl font-bold text-gray-900">{totalWords}</div>
        </div>
        
        {Object.entries(metrics.word_counts).map(([key, count]) => (
          <div key={key} className="bg-white p-3 rounded border border-gray-200">
            <div className="text-xs text-gray-500 mb-1 truncate" title={key}>
              {formatLabel(key)}
            </div>
            <div className="text-lg font-semibold text-gray-700">{count}</div>
          </div>
        ))}
      </div>

      {metrics.warnings && metrics.warnings.length > 0 && (
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
          <h5 className="text-sm font-semibold text-yellow-900 mb-2">
            Ostrzeżenia ({metrics.warnings.length})
          </h5>
          <ul className="list-disc list-inside space-y-1">
            {metrics.warnings.map((warning, index) => (
              <li key={index} className="text-sm text-yellow-800">
                {warning}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-3 text-xs text-gray-500">
        <p>
          <strong>Standard Turris:</strong> {stepName === 'Step 1' ? '900-1,500 słów' : 
          stepName.startsWith('Step 2') ? '1,050-1,500 słów per proces' : 
          stepName.startsWith('Step 3') ? '1,100-1,600 słów per proces' : 
          '1,000-1,500 słów'}
        </p>
      </div>
    </div>
  );
};

function formatLabel(key: string): string {
  const labels: Record<string, string> = {
    'total': 'Całkowita',
    'executive_summary': 'Executive Summary',
    'legal_analysis': 'Analiza prawna',
    'top_processes': 'TOP procesy',
    'recommendations': 'Rekomendacje',
    'bpmn_description': 'Opis BPMN',
    'bottlenecks': 'Wąskie gardła',
    'muda_analysis': 'Analiza MUDA',
    'automation_rationale': 'Potencjał automatyzacji',
    'comparison': 'Porównanie'
  };

  return labels[key] || key.replace(/_/g, ' ');
}
