import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, FolderOpen, Trash2, Clock } from 'lucide-react';
import { projectsAPI } from '../services/api';
import { useToastStore } from '../store/toastStore';
import ConfirmDialog from '../components/ConfirmDialog';
import LoadingSpinner from '../components/LoadingSpinner';
import type { Project } from '../types';

export default function Dashboard() {
  const navigate = useNavigate();
  const toast = useToastStore();
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newClientName, setNewClientName] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState<{ show: boolean; projectId: number | null }>({
    show: false,
    projectId: null,
  });

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await projectsAPI.getAll();
      setProjects(data);
    } catch (error) {
      console.error('Error loading projects:', error);
      toast.error('Nie udało się załadować projektów');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const project = await projectsAPI.create({
        name: newProjectName,
        client_name: newClientName,
      });
      setShowCreateModal(false);
      setNewProjectName('');
      setNewClientName('');
      toast.success('Projekt utworzony pomyślnie!');
      navigate(`/project/${project.id}`);
    } catch (error: any) {
      console.error('Error creating project:', error);
      toast.error(error.response?.data?.message || 'Nie udało się utworzyć projektu');
    }
  };

  const handleDeleteProject = async (id: number) => {
    setDeleteConfirm({ show: true, projectId: id });
  };

  const confirmDelete = async () => {
    if (!deleteConfirm.projectId) return;
    
    try {
      await projectsAPI.delete(deleteConfirm.projectId);
      toast.success('Projekt usunięty');
      loadProjects();
    } catch (error: any) {
      console.error('Error deleting project:', error);
      toast.error(error.response?.data?.message || 'Nie udało się usunąć projektu');
    } finally {
      setDeleteConfirm({ show: false, projectId: null });
    }
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      step1: 'Krok 1: Analiza wstępna',
      step2: 'Krok 2: Mapowanie procesów',
      step3: 'Krok 3: Rekomendacje',
      step4: 'Krok 4: Generowanie',
      completed: 'Zakończony',
    };
    return labels[status] || status;
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      step1: 'bg-blue-500',
      step2: 'bg-yellow-500',
      step3: 'bg-orange-500',
      step4: 'bg-purple-500',
      completed: 'bg-primary-500',
    };
    return colors[status] || 'bg-gray-500';
  };

  if (isLoading) {
    return <LoadingSpinner message="Ładowanie projektów..." />;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Twoje Projekty Audytowe</h1>
          <p className="text-gray-400">Zarządzaj audytami automatyzacyjnymi BFA</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Nowy Projekt</span>
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="card text-center py-12">
          <FolderOpen className="w-16 h-16 text-gray-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-300 mb-2">
            Brak projektów
          </h3>
          <p className="text-gray-500 mb-4">
            Rozpocznij swój pierwszy audyt automatyzacyjny
          </p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary"
          >
            Utwórz Projekt
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div key={project.id} className="card hover:border-primary-500 transition-colors cursor-pointer group">
              <div onClick={() => navigate(`/project/${project.id}`)}>
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-white mb-1 group-hover:text-primary-500">
                      {project.name}
                    </h3>
                    <p className="text-gray-400 text-sm">{project.client_name}</p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteProject(project.id);
                    }}
                    className="p-2 text-gray-500 hover:text-red-500 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="flex items-center space-x-2 mb-3">
                  <div className={`w-2 h-2 rounded-full ${getStatusColor(project.status)}`}></div>
                  <span className="text-sm text-gray-400">{getStatusLabel(project.status)}</span>
                </div>

                <div className="flex items-center text-xs text-gray-500">
                  <Clock className="w-4 h-4 mr-1" />
                  <span>
                    {new Date(project.updated_at).toLocaleDateString('pl-PL')}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Project Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="card max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold text-white mb-6">Nowy Projekt Audytowy</h2>
            <form onSubmit={handleCreateProject} className="space-y-4">
              <div>
                <label className="label">Nazwa projektu</label>
                <input
                  type="text"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  className="input"
                  placeholder="np. Audyt Q1 2024"
                  required
                />
              </div>

              <div>
                <label className="label">Nazwa klienta</label>
                <input
                  type="text"
                  value={newClientName}
                  onChange={(e) => setNewClientName(e.target.value)}
                  className="input"
                  placeholder="np. ACME Corporation"
                  required
                />
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    setNewProjectName('');
                    setNewClientName('');
                  }}
                  className="btn btn-secondary flex-1"
                >
                  Anuluj
                </button>
                <button type="submit" className="btn btn-primary flex-1">
                  Utwórz
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      {deleteConfirm.show && (
        <ConfirmDialog
          title="Usuń Projekt"
          message="Czy na pewno chcesz usunąć ten projekt? Ta operacja jest nieodwracalna i usunie wszystkie dane audytowe."
          confirmLabel="Usuń"
          cancelLabel="Anuluj"
          variant="danger"
          onConfirm={confirmDelete}
          onCancel={() => setDeleteConfirm({ show: false, projectId: null })}
        />
      )}
    </div>
  );
}
