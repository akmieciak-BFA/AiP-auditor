import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle } from 'lucide-react';
import { projectsAPI } from '../services/api';
import type { Project } from '../types';
import Step1Form from '../components/Step1Form';
import Step2Form from '../components/Step2Form';
import Step3Form from '../components/Step3Form';
import Step4Form from '../components/Step4Form';
import { DownloadButton } from '../components/DownloadButton';

export default function ProjectView() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState<string>('step1');

  useEffect(() => {
    loadProject();
  }, [id]);

  const loadProject = async () => {
    if (!id) return;
    
    try {
      const data = await projectsAPI.getOne(parseInt(id));
      setProject(data);
      setCurrentStep(data.status);
    } catch (error) {
      console.error('Error loading project:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const steps = [
    { key: 'step1', label: 'Analiza Wstępna', number: 1 },
    { key: 'step2', label: 'Mapowanie Procesów', number: 2 },
    { key: 'step3', label: 'Rekomendacje', number: 3 },
    { key: 'step4', label: 'Generowanie', number: 4 },
  ];

  const getStepStatus = (stepKey: string) => {
    const stepIndex = steps.findIndex((s) => s.key === stepKey);
    const currentIndex = steps.findIndex((s) => s.key === currentStep);
    
    if (stepIndex < currentIndex || project?.status === 'completed') {
      return 'completed';
    } else if (stepIndex === currentIndex) {
      return 'current';
    }
    return 'upcoming';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Ładowanie projektu...</div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-300 mb-4">Projekt nie znaleziony</h2>
        <button onClick={() => navigate('/')} className="btn btn-primary">
          Powrót do Dashboard
        </button>
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={() => navigate('/')}
        className="flex items-center space-x-2 text-gray-400 hover:text-white mb-6"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Powrót do Dashboard</span>
      </button>

      <div className="mb-8">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">{project.name}</h1>
            <p className="text-gray-400">Klient: {project.client_name}</p>
          </div>
          
          {/* Download Button - show if project has any data beyond step1 */}
          {(project.status !== 'step1' || currentStep !== 'step1') && (
            <div className="flex gap-2">
              <DownloadButton
                projectId={project.id}
                projectName={project.name}
                clientName={project.client_name}
                variant="outline"
                size="md"
              />
            </div>
          )}
        </div>
      </div>

      {/* Progress Steps */}
      <div className="card mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => {
            const status = getStepStatus(step.key);
            return (
              <div key={step.key} className="flex items-center flex-1">
                <div className="flex flex-col items-center flex-1">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all ${
                      status === 'completed'
                        ? 'bg-primary-500 border-primary-500'
                        : status === 'current'
                        ? 'bg-dark-700 border-primary-500'
                        : 'bg-dark-700 border-dark-600'
                    }`}
                  >
                    {status === 'completed' ? (
                      <CheckCircle className="w-6 h-6 text-dark-900" />
                    ) : (
                      <span
                        className={`text-lg font-bold ${
                          status === 'current' ? 'text-primary-500' : 'text-gray-500'
                        }`}
                      >
                        {step.number}
                      </span>
                    )}
                  </div>
                  <div className="mt-2 text-center">
                    <div
                      className={`text-sm font-medium ${
                        status === 'current' ? 'text-primary-500' : 'text-gray-400'
                      }`}
                    >
                      Krok {step.number}
                    </div>
                    <div className="text-xs text-gray-500">{step.label}</div>
                  </div>
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={`h-0.5 flex-1 ${
                      status === 'completed' ? 'bg-primary-500' : 'bg-dark-600'
                    }`}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Step Content */}
      <div className="card">
        {currentStep === 'step1' && (
          <Step1Form projectId={project.id} onComplete={() => loadProject()} />
        )}
        {currentStep === 'step2' && (
          <Step2Form projectId={project.id} onComplete={() => loadProject()} />
        )}
        {currentStep === 'step3' && (
          <Step3Form projectId={project.id} onComplete={() => loadProject()} />
        )}
        {(currentStep === 'step4' || currentStep === 'completed') && (
          <Step4Form projectId={project.id} onComplete={() => loadProject()} />
        )}
      </div>
    </div>
  );
}
