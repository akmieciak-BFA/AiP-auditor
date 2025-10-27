import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useToastStore } from './store/toastStore';
import ErrorBoundary from './components/ErrorBoundary';
import { ToastContainer } from './components/Toast';
import Dashboard from './pages/Dashboard';
import ProjectView from './pages/ProjectView';
import Layout from './components/Layout';

function App() {
  const { toasts, removeToast } = useToastStore();

  return (
    <ErrorBoundary>
      <Router>
        <ToastContainer toasts={toasts} onRemove={removeToast} />
        <Routes>
          <Route
            path="/"
            element={
              <Layout>
                <Dashboard />
              </Layout>
            }
          />
          <Route
            path="/project/:id"
            element={
              <Layout>
                <ProjectView />
              </Layout>
            }
          />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
