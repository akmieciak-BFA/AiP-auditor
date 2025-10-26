import styled from 'styled-components';
import { Header } from './components/Header';
import { Dashboard } from './components/Dashboard';
import { Footer } from './components/Footer';
import './styles/global.css';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

function App() {
  return (
    <AppContainer>
      <Header />
      <Dashboard />
      <Footer />
    </AppContainer>
  );
}

export default App;
