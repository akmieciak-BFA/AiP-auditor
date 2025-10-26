import { lazy, Suspense } from 'react';
import styled from 'styled-components';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import './styles/global.css';

// Lazy load components for better performance
const Header = lazy(() => import('./components/Header').then(module => ({ default: module.Header })));
const Dashboard = lazy(() => import('./components/Dashboard').then(module => ({ default: module.Dashboard })));
const Footer = lazy(() => import('./components/Footer').then(module => ({ default: module.Footer })));

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

const LoadingContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  font-size: 1.125rem;
  color: #6B7280;
`;

// Loading fallback component
const LoadingFallback = () => (
  <LoadingContainer role="status" aria-live="polite">
    <div>Ładowanie...</div>
  </LoadingContainer>
);

function App() {
  return (
    <ErrorBoundary>
      <AppContainer>
        <Suspense fallback={<LoadingFallback />}>
          <Header />
        </Suspense>
        <Suspense fallback={<LoadingFallback />}>
          <Dashboard />
        </Suspense>
        <Suspense fallback={<LoadingFallback />}>
          <Footer />
        </Suspense>
      </AppContainer>
    </ErrorBoundary>
  );
}

export default App;
