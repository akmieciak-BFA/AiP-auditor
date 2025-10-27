import { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, FolderOpen, Trash2, Clock, Search, Filter } from 'lucide-react';
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
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'name' | 'client_name' | 'updated_at'>('updated_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [deleteConfirm, setDeleteConfirm] = useState<{ show: boolean; projectId: number | null }>({
    show: false,
    projectId: null,
  });

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await projectsAPI.getAll();
      setProjects(data);
    } catch (error) {
      console.error('Error loading projects:', error);
      toast.error('Nie udało się załadować projektów');
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

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

  // Filtered and sorted projects
  const filteredProjects = useMemo(() => {
    let filtered = projects;

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(
        (project) =>
          project.name.toLowerCase().includes(term) ||
          project.client_name.toLowerCase().includes(term)
      );
    }

    // Apply status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter((project) => project.status === statusFilter);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: string | number;
      let bValue: string | number;

      if (sortBy === 'updated_at') {
        aValue = new Date(a.updated_at).getTime();
        bValue = new Date(b.updated_at).getTime();
      } else {
        aValue = a[sortBy].toLowerCase();
        bValue = b[sortBy].toLowerCase();
      }

      if (sortOrder === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });

    return filtered;
  }, [projects, searchTerm, statusFilter, sortBy, sortOrder]);

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

      {/* Search and Filter Controls */}
      <div className="card mb-6 p-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Szukaj projektów..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10 w-full"
              />
            </div>
          </div>

          {/* Status Filter */}
          <div className="flex gap-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input"
            >
              <option value="all">Wszystkie statusy</option>
              <option value="step1">Krok 1</option>
              <option value="step2">Krok 2</option>
              <option value="step3">Krok 3</option>
              <option value="step4">Krok 4</option>
              <option value="completed">Zakończone</option>
            </select>

            {/* Sort Controls */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'name' | 'client_name' | 'updated_at')}
              className="input"
            >
              <option value="updated_at">Data aktualizacji</option>
              <option value="name">Nazwa projektu</option>
              <option value="client_name">Nazwa klienta</option>
            </select>

            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="btn btn-secondary flex items-center space-x-1"
              title={`Sortuj ${sortOrder === 'asc' ? 'malejąco' : 'rosnąco'}`}
            >
              <Filter className="w-4 h-4" />
              <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
            </button>
          </div>
        </div>
        
        {/* Project Count */}
        <div className="text-sm text-gray-400 mt-2">
          {filteredProjects.length} z {projects.length} projektów
        </div>
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
      ) : filteredProjects.length === 0 ? (
        <div className="card text-center py-12">
          <Search className="w-16 h-16 text-gray-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-300 mb-2">
            Nie znaleziono projektów
          </h3>
          <p className="text-gray-500 mb-4">
            Spróbuj zmienić kryteria wyszukiwania lub filtrowania
          </p>
          <button
            onClick={() => {
              setSearchTerm('');
              setStatusFilter('all');
            }}
            className="btn btn-secondary"
          >
            Wyczyść filtry
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project) => (
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
